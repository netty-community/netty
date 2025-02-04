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

from dataclasses import dataclass
from typing import ClassVar
from pathlib import Path

from pydantic import IPvAnyInterface, IPvAnyAddress

from netty.arch import DeviceType
from netty.project import LanNetwork, WanNetwork, WebFilter, Device, PhysicalInterface
from netty.project.config import BaselineConfig, SnmpConfig, SystemConfig
from netty._types import FirewallWanHAMode
from netty.consts import DEFAULT_CONFIG_OUTPUT_PATH


@dataclass
class Firewall:
    hostname: str
    lan_ip: IPvAnyInterface
    lan_gateway: IPvAnyAddress
    lan_networks: list[LanNetwork]
    wan_networks: WanNetwork
    enable_ha: bool
    device_type: DeviceType
    baseline_config: "BaselineConfig"
    snmp_config: SnmpConfig
    system_config: SystemConfig
    firewall_working_mode: FirewallWanHAMode
    web_filters: WebFilter | None = None

    @property
    def lan_addr_str(self) -> str:
        lan_str = ""
        for lan in self.lan_networks:
            lan_str += f'"{lan.network}" '
        return lan_str


class FirewallFactory:
    default_jinja_template_path: ClassVar[Path] = Path()
    default_jinja_template_name: ClassVar[str] = "switch.j2"

    def __init__(
        self,
        device: Device,
        baseline_config: "BaselineConfig",
        snmp_config: "SnmpConfig",
        system_config: "SystemConfig",
        interfaces: list[PhysicalInterface],
    ) -> None:
        self.device = device
        self.baseline_config = baseline_config
        self.snmp_config = snmp_config
        self.system_config = system_config
        self.interfaces = interfaces

    def enrich_data(self) -> Firewall:
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
