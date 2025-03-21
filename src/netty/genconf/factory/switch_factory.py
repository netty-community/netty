"""Copyright 2024 wangxin.jeffry@gmail.com
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http:www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, ClassVar
from ipaddress import IPv4Network, IPv4Address, IPv4Interface

from pydantic import PositiveInt

from netty.arch import DeviceRole
from netty.project import FixedIP, Device, Subnet, PhysicalInterface, StackPort
from netty._types import IfMode
from netty.project.config import (
    AAAConfig,
    BaselineConfig,
    NetflowConfig,
    SnmpConfig,
    SystemConfig,
)

from netty.consts import DEFAULT_CONFIG_OUTPUT_PATH


@dataclass
class Stp:
    stp_root: bool
    stp_priority: int


@dataclass
class Vlan:
    vlan_id: int
    vlan_name: str | None = None


@dataclass
class Vrf:
    vrf_name: str
    family: Literal[4, 6]


@dataclass
class VlanIf:
    vlan_id: PositiveInt
    network: IPv4Network
    gateway: IPv4Address
    vlan_name: str | None = None
    vrf_name: str | None = None
    enable_dhcp: bool = False


@dataclass
class DHCPExcludeRange:
    range_start: IPv4Address
    range_end: IPv4Address


@dataclass
class DHCPPool:
    dhcp_pool_name: str
    dhcp_pool_network: IPv4Network
    dhcp_pool_gateway: IPv4Interface
    dhcp_pool_dns_server: list[IPv4Address]
    dhcp_pool_range_start: IPv4Address | None = None
    dhcp_pool_range_end: IPv4Address | None = None
    dhcp_pool_lease_time: int = 86400
    fixed_ips: list["FixedIP"] = field(default_factory=lambda: [])
    # it's only for cisco
    exclude_ranges: list["DHCPExcludeRange"] = field(default_factory=lambda: [])


@dataclass
class PortChannel:
    port_channel_id: int | str
    if_mode: IfMode
    if_descr: str | None = None
    vlan_id: int | None = None
    dhcp_snooping_enable: bool = False
    dhcp_snooping_trust: bool = False
    enable_netflow: bool = False


@dataclass
class Switch:
    hostname: str
    site_code: str
    baseline_config: "BaselineConfig"
    snmp_config: "SnmpConfig"
    system_config: "SystemConfig"
    netflow_config: "NetflowConfig"
    stack_config: "StackPort | None" = None
    enable_stack: bool = False
    enable_guest_acl: bool = False
    dhcp_pools: list["DHCPPool"] | None = None
    aaa_config: "AAAConfig | None" = None
    stp_config: "Stp | None" = None
    vlans: list["Vlan"] | None = None
    vlan_ifs: list["VlanIf"] | None = None
    routed_ifs: list["PhysicalInterface"] | None = None
    physical_ifs: list["PhysicalInterface"] | None = None
    port_channels: list["PortChannel"] | None = None
    vrfs: list["Vrf"] | None = None
    default_gateway: IPv4Address | None = None

    def __setattr__(self, name: str, value: Any) -> None:
        """used for vendor customized fields only"""
        if value is not None:
            self.__dict__[name] = value


class SwitchFactory:
    default_jinja_template_path: ClassVar[Path] = Path()
    default_jinja_template_name: ClassVar[str] = "switch.j2"

    def __init__(
        self,
        site_code: str,
        device: Device,
        baseline_config: "BaselineConfig",
        snmp_config: "SnmpConfig",
        system_config: "SystemConfig",
        netflow_config: "NetflowConfig",
        aaa_config: "AAAConfig | None" = None,
        subnets: list[Subnet] | None = None,
        fixed_ips: list[FixedIP] | None = None,
    ) -> None:
        self.site_code = site_code
        self.device = device
        self.baseline_config = baseline_config
        self.snmp_config = snmp_config
        self.system_config = system_config
        self.netflow_config = netflow_config
        self.aaa_config = aaa_config
        self.subnets = subnets
        self.fixed_ips = fixed_ips

    def get_vlan_list(self) -> list[Vlan]:
        if not self.subnets:
            return []
        return [
            Vlan(vlan_id=subnet.vlan_id, vlan_name=subnet.name)
            for subnet in self.subnets
            if subnet.vlan_id
        ]

    def get_dhcp_pool_list(self) -> list[DHCPPool]:
        if not self.subnets or self.device.device_role != DeviceRole.core_switch:
            return []
        results: list[DHCPPool] = []
        for subnet in self.subnets:
            if subnet.dhcp_pool and subnet.dhcp_network:
                dhcp_config = DHCPPool(
                    dhcp_pool_name=f"vlan{subnet.vlan_id}",
                    dhcp_pool_network=subnet.dhcp_network,
                    dhcp_pool_range_start=subnet.dhcp_range_start,
                    dhcp_pool_range_end=subnet.dhcp_range_end,
                    dhcp_pool_dns_server=subnet.dns_server,
                    dhcp_pool_gateway=subnet.if_addr,
                    fixed_ips=[],
                )
                if not self.fixed_ips:
                    pass
                else:
                    for ip in self.fixed_ips:
                        if ip.ip.network == subnet.dhcp_network:
                            dhcp_config.fixed_ips.append(ip)
                results.append(dhcp_config)
        return results

    def get_vlan_if_list(self) -> list["VlanIf"]:
        if not self.subnets:
            return []
        if self.device.device_role == DeviceRole.core_switch:
            return [
                VlanIf(
                    vlan_id=subnet.vlan_id,
                    vlan_name=subnet.name,
                    network=subnet.if_addr.network,
                    gateway=subnet.if_addr,
                    vrf_name=subnet.vrf_name,
                    enable_dhcp=True
                    if subnet.dhcp_pool and subnet.dhcp_network
                    else False,
                )
                for subnet in self.subnets
                if subnet.vlan_id
            ]
        return [
            VlanIf(
                vlan_id=subnet.vlan_id,
                vlan_name=subnet.name,
                network=subnet.if_addr.network,
                gateway=subnet.if_addr,
                vrf_name=subnet.vrf_name,
                enable_dhcp=True if subnet.dhcp_pool and subnet.dhcp_network else False,
            )
            for subnet in self.subnets
            if subnet.vlan_id and subnet.vlan_id == self.system_config.management_vlan
        ]

    def get_vrf_list(self) -> list["Vrf"]:
        if not self.subnets:
            return []
        if self.device.device_role == DeviceRole.core_switch:
            return [
                Vrf(vrf_name=subnet.vrf_name, family=subnet.if_addr.version)
                for subnet in self.subnets
                if subnet.vrf_name
            ]
        return []

    def get_l3_interface_list(self) -> list["PhysicalInterface"]:
        if not self.subnets:
            return []
        if self.device.device_role == DeviceRole.core_switch:
            interfaces = [
                PhysicalInterface(
                    if_name=subnet.interface_name,
                    if_descr=subnet.name,
                    if_addr=subnet.if_addr,
                    if_mode="routed",
                    vrf_name=subnet.vrf_name,
                )
                for subnet in self.subnets
                if subnet.interface_name and not subnet.vlan_id and subnet.if_addr
            ]
        else:
            interfaces = []
        return interfaces

    def get_port_channel_list(self) -> list["PortChannel"]:
        if not self.device.interfaces:
            return []
        unique_port_channels = []
        results = []
        for interface in self.device.interfaces:
            if interface.port_channel_id is None:
                continue
            if interface.port_channel_id not in unique_port_channels:
                results.append(
                    PortChannel(
                        port_channel_id=interface.port_channel_id,
                        if_mode=interface.if_mode,
                        if_descr=interface.port_channel_descr,
                        dhcp_snooping_enable=interface.dhcp_snooping_enable,
                        dhcp_snooping_trust=interface.dhcp_snooping_trust,
                        enable_netflow=interface.enable_netflow,
                        vlan_id=interface.vlan_id,
                    )
                )
                unique_port_channels.append(interface.port_channel_id)
                if interface.enable_netflow:
                    interface.enable_netflow = False
        return results

    def enrich_data(self) -> Switch:
        raise NotImplementedError

    def load_jinja2_template(self) -> str:
        raise NotImplementedError

    def generate_config(self) -> str:
        raise NotImplementedError

    def generate_config_file(self) -> None:
        file = Path(f"{DEFAULT_CONFIG_OUTPUT_PATH}/{self.device.hostname}.ios")
        file.parent.mkdir(parents=True, exist_ok=True)
        with Path.open(file, "w") as f:
            f.write(self.generate_config())
