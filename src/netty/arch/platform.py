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


class Platform(StrEnum):
    cisco_xe = "cisco_xe"
    huawei_vrp = "huawei_vrp"
    ruijie_os = "ruijie_os"
    aruba_os = "aruba_os"
    fortinet = "fortinet"

    @classmethod
    def manufacturer(cls, platform: "Platform") -> "Manufacturer":
        mapping = {
            cls.cisco_xe: Manufacturer.cisco,
            cls.huawei_vrp: Manufacturer.huawei,
            cls.ruijie_os: Manufacturer.ruijie,
            cls.aruba_os: Manufacturer.aruba,
            cls.fortinet: Manufacturer.fortinet,
        }
        manufacturer = mapping.get(platform)
        if manufacturer is None:
            msg = f"Unknown platform: {platform}"
            raise ValueError(msg)
        return manufacturer
    
    @classmethod
    def port_channel_prefix(cls, platform: "Platform")-> "PortChannelPrefix":
        mapping = {
            cls.cisco_xe: PortChannelPrefix.cisco,
            cls.huawei_vrp: PortChannelPrefix.huawei,
            cls.ruijie_os: PortChannelPrefix.ruijie,
            cls.aruba_os: PortChannelPrefix.aruba,
            cls.fortinet: PortChannelPrefix.fortinet,
        }
        prefix = mapping.get(platform)
        if prefix is None:
            msg = f"Unknown platform: {platform}"
            raise ValueError(msg)
        return prefix 


class Manufacturer(StrEnum):
    cisco = "Cisco"
    huawei = "Huawei"
    ruijie = "Ruijie"
    aruba = "HPE"
    fortinet = "Fortinet"


class PortChannelPrefix(StrEnum):
    cisco = "Po"
    huawei = "Eth"
    ruijie = "Agg"
    aruba = "Po"
    fortinet = "agg"