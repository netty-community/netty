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

from enum import StrEnum
from dataclasses import dataclass


class Platform(StrEnum):
    cisco_xe = "cisco_xe"
    cisco_nxos = "cisco_nxos"
    huawei_vrp = "huawei_vrp"
    ruijie_os = "ruijie_os"
    aruba_os = "aruba_os"
    fortinet = "fortinet"
    paloalto = "paloalto"

    @property
    def manufacturer(self) -> "Manufacturer":
        mapping = {
            Platform.cisco_xe: Manufacturer.cisco,
            Platform.cisco_nxos: Manufacturer.cisco,
            Platform.huawei_vrp: Manufacturer.huawei,
            Platform.ruijie_os: Manufacturer.ruijie,
            Platform.aruba_os: Manufacturer.aruba,
            Platform.fortinet: Manufacturer.fortinet,
            Platform.paloalto: Manufacturer.paloalto,
        }
        manufacturer = mapping.get(self)
        if manufacturer is None:
            msg = f"Unknown platform: {self}"
            raise ValueError(msg)
        return manufacturer

    @property
    def port_channel_prefix(self) -> "PortChannelPrefix":
        mapping = {
            Platform.cisco_xe: PortChannelPrefix.cisco,
            Platform.cisco_nxos: PortChannelPrefix.cisco,
            Platform.huawei_vrp: PortChannelPrefix.huawei,
            Platform.ruijie_os: PortChannelPrefix.ruijie,
            Platform.aruba_os: PortChannelPrefix.aruba,
            Platform.fortinet: PortChannelPrefix.fortinet,
            Platform.paloalto: PortChannelPrefix.paloalto,
        }
        prefix = mapping.get(self)
        if prefix is None:
            msg = f"Unknown platform: {self}"
            raise ValueError(msg)
        return prefix


class Manufacturer(StrEnum):
    cisco = "Cisco"
    huawei = "Huawei"
    ruijie = "Ruijie"
    aruba = "HOPE"
    fortinet = "Fortinet"
    paloalto = "PaloAlto"

    @classmethod
    def to_list_str(cls):
        return [v.value for v in cls]


class PortChannelPrefix(StrEnum):
    cisco = "Po"
    huawei = "Eth"
    ruijie = "Agg"
    aruba = "Po"
    fortinet = ""
    paloalto = "AE"

@dataclass
class PlatformView:
    name: str
    manufacturer: Manufacturer
    port_channel_prefix: PortChannelPrefix


def get_platform_views() -> list[PlatformView]:
    return [
        PlatformView(name=platform.value, manufacturer=platform.manufacturer, port_channel_prefix=platform.port_channel_prefix)
        for platform in Platform
    ]
