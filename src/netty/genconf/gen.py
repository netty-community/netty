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
from ipaddress import IPv4Address


from netty.project import (
    Device,
    Subnet,
    FixedIP,
    PhysicalInterface,
    Connection,
    Project,
)
from netty.arch import (
    DeviceRole,
    ProductFamily,
    generate_if_mode,
    enable_if_port_fast,
    enable_if_dhcp_snooping,
    enable_if_dhcp_snooping_trust,
    enable_if_netflow_export,
)
from netty.genconf.factory.switch_factory import SwitchFactory
from netty.consts import PROJECT_CONFIG
from netty.project.config import settings
from netty.genconf.dispatcher import get_switch_factory
from netty.genconf.utils import (
    remove_duplicate_devices,
    generate_default_gateway,
    remove_stack_ports,
)
from netty.utils.netif import generate_port_channel_descr


def __hostname_to_ip(devices: list[Device]) -> dict[str, IPv4Address]:
    hostname_to_ip: dict[str, IPv4Address] = {
        device.hostname: device.management_ip for device in devices
    }
    return hostname_to_ip


def __ip_to_device(devices: list[Device]) -> dict[IPv4Address, Device]:
    ip_to_device: dict[IPv4Address, Device] = {}
    unique_devices = remove_duplicate_devices(devices)
    for device in unique_devices:
        ip_to_device[device.management_ip] = device
    return ip_to_device


def __link_connections_to_device(
    devices: list[Device], connections: list[Connection]
) -> list[Device]:
    ip_to_device_map = __ip_to_device(devices)
    hostname_to_ip_map = __hostname_to_ip(devices)
    if not connections:
        return []
    for connection in connections:
        local_ip = hostname_to_ip_map.get(connection.local_hostname)
        remote_ip = hostname_to_ip_map.get(connection.remote_hostname)
        if local_ip is None:
            raise ValueError(
                f"Device with hostname {connection.local_hostname} not found"
            )
        local_device = ip_to_device_map[local_ip]
        if remote_ip is not None:
            remote_device = ip_to_device_map[remote_ip]
            local_if_mode = generate_if_mode(
                local_device.device_role, remote_device.device_role
            )
            remote_if_mode = generate_if_mode(
                remote_device.device_role, local_device.device_role
            )

            local_device.interfaces.append(
                PhysicalInterface(
                    if_name=connection.local_interface_name,
                    if_descr=connection.local_if_descr,
                    port_channel_descr=generate_port_channel_descr(
                        connection.local_port_channel_descr,
                        remote_device.device_type.platform.port_channel_prefix
                    ),
                    if_mode=local_if_mode,
                    enable_netflow=enable_if_netflow_export(
                        local_device.device_role,
                        remote_device.device_role
                    ),
                    port_channel_id=connection.local_port_channel_id,
                    dhcp_snooping_enable=enable_if_dhcp_snooping(
                        local_device.device_role, local_if_mode
                    ),
                    dhcp_snooping_trust=enable_if_dhcp_snooping_trust(
                        local_device.device_role, remote_device.device_role
                    ),
                    port_fast=enable_if_port_fast(
                        local_device.device_role, local_if_mode
                    ),
                )
            )

            remote_device.interfaces.append(
                PhysicalInterface(
                    if_name=connection.remote_interface_name,
                    if_descr=connection.remote_if_descr,
                    port_channel_descr=generate_port_channel_descr(
                        connection.remote_port_channel_descr,
                        local_device.device_type.platform.port_channel_prefix
                    ),
                    if_mode=remote_if_mode,
                    enable_netflow=enable_if_netflow_export(
                        remote_device.device_role,
                        local_device.device_role,
                    ),
                    port_channel_id=connection.remote_port_channel_id,
                    dhcp_snooping_enable=enable_if_dhcp_snooping(
                        remote_device.device_role, remote_if_mode
                    ),
                    dhcp_snooping_trust=enable_if_dhcp_snooping_trust(
                        remote_device.device_role, local_device.device_role
                    ),
                    port_fast=enable_if_port_fast(
                        remote_device.device_role, remote_if_mode
                    ),
                )
            )
        elif local_device.device_role in (
            DeviceRole.firewall,
            DeviceRole.internet_switch,
        ):
            local_device.interfaces.append(
                PhysicalInterface(
                    if_name=connection.local_interface_name,
                    if_descr=connection.local_if_descr,
                    port_channel_descr=generate_port_channel_descr(
                        connection.local_port_channel_descr,
                        remote_device.device_type.platform.port_channel_prefix
                    ),
                    if_mode="access",
                    enable_netflow=False,  # Assuming no netflow for standalone firewall interface
                    port_channel_id=connection.local_port_channel_id,
                    dhcp_snooping_enable=False,  # Assuming no DHCP snooping for standalone firewall interface
                    dhcp_snooping_trust=False,  # Assuming no DHCP snooping trust for standalone firewall interface
                    port_fast=False,  # Assuming no port fast for standalone firewall interface
                )
            )
        else:
            raise ValueError(
                f"Remote device with hostname {connection.remote_hostname} not found"
            )
    return list(ip_to_device_map.values())


def switch_config_generator(
    factory: type[SwitchFactory],
    device: Device,
    subnets: list[Subnet] | None = None,
    fixed_ips: list[FixedIP] | None = None,
) -> None:
    new_device = factory(
        site_code=PROJECT_CONFIG.site_code,
        device=device,
        baseline_config=settings.baseline_config,
        snmp_config=settings.snmp_config,
        system_config=settings.system_config,
        netflow_config=settings.netflow_config,
        aaa_config=settings.aaa_config,
        subnets=subnets,
        fixed_ips=fixed_ips,
    )
    return new_device.generate_config_file()


def _switch_gen(
    device: Device,
    subnets: list[Subnet] | None = None,
    fixed_ips: list[FixedIP] | None = None,
) -> None:
    if "switch" in device.device_role.lower():
        factory = get_switch_factory(device)
        if not factory:
            return None
        return switch_config_generator(factory, device, subnets, fixed_ips)
    return None


def _firewall_gen(device: Device, project_info: Project): ...


def config_generator(devices: list[Device], connections: list[Connection], subnets: list[Subnet], fix_ips: list[FixedIP], project_info: Project) -> None:
    if connections:
        connections, devices = remove_stack_ports(devices, connections)
        devices = __link_connections_to_device(devices, connections)
    for device in devices:
        if not device.default_gateway:
            device.default_gateway = generate_default_gateway(devices, device)
        if device.device_type.product_family == ProductFamily.switch:
            _switch_gen(device, subnets, fix_ips)
        elif device.device_type.product_family == ProductFamily.firewall:
            _firewall_gen(device, project_info=project_info)
        else:
            _switch_gen(device)
