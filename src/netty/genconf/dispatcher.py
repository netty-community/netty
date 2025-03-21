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

from netty.arch import Platform, ProductFamily
from netty.project import Device
from netty.genconf.factory.switch_factory import SwitchFactory
# from netty.genconf.factory.firewall_factory import FirewallFactory

from netty.genconf.manufacturer.ruijie.switch import RuijieSwitch
from netty.genconf.manufacturer.huawei.switch import HuaweiSwitch
from netty.genconf.manufacturer.cisco.switch import CiscoSwitch


def get_switch_factory(device: Device) -> type[SwitchFactory] | None:
    if (
        device.device_type.platform == Platform.ruijie_os
        and device.device_type.product_family == ProductFamily.switch
    ):
        return RuijieSwitch
    if (
        device.device_type.platform == Platform.huawei_vrp
        and device.device_type.product_family == ProductFamily.switch
    ):
        return HuaweiSwitch
    if (
        device.device_type.platform == Platform.cisco_xe
        and device.device_type.product_family == ProductFamily.switch
    ):
        return CiscoSwitch
    return None


# def get_firewall_factory(device: Device) -> type[FirewallFactory] | None:
#     if (
#         device.device_type.platform == Platform.fortinet
#         and device.device_type.product_family == ProductFamily.firewall
#     ):
#         return FortinetFirewall
#     return None
