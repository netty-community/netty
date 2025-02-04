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


from netty._types import IfMode


class DeviceRole(StrEnum):
    internet = "Internet"  # internet role is only used for topology generation, not for config generation
    core_switch = "Core Switch"
    distributed_switch = "Distribution Switch"
    access_switch = "Access Switch"
    internet_switch = "Internet Switch"
    wlan_ac = "WLAN AC"
    firewall = "Firewall"
    wlan_ap = "Access Point"
    wan_router = "WAN Router"
    sdwan_hub = "SD-WAN Hub"

    @classmethod
    def to_list_str(cls) -> list[str]:
        return [role.value for role in cls]

    @property
    def stp_root(self) -> tuple[bool, int]:
        if self == DeviceRole.core_switch:
            return True, 4096
        return False, 32768

    @property
    def stp_edge_optimize(self) -> bool:
        return self == DeviceRole.access_switch

    @property
    def enable_guest_acl(self) -> bool:
        return self == DeviceRole.core_switch

    @property
    def node_level(self) -> int:
        match self:
            case DeviceRole.internet:
                return 1
            case DeviceRole.internet_switch:
                return 2
            case DeviceRole.firewall:
                return 3
            case DeviceRole.core_switch | DeviceRole.wlan_ac:
                return 4
            case DeviceRole.distributed_switch:
                return 5
            case DeviceRole.access_switch:
                return 6
            case DeviceRole.wlan_ap:
                return 7
            case _:
                return 8

    @property
    def drawio_style(self) -> dict[str, str]:
        match self:
            case DeviceRole.internet:
                return {
                    "style": "ellipse;shape=cloud;whiteSpace=wrap;html=1;fontSize=10",
                    "width": "120",
                    "height": "80",
                }
            case DeviceRole.core_switch:
                return {
                    "style": "shape=mxgraph.cisco19.rect;prIcon=l3_switch;fillColor=#FAFAFA;strokeColor=#005073;html=1;fontSize=10;",
                    "width": "50",
                    "height": "50",
                }
            case DeviceRole.distributed_switch:
                return {
                    "style": "shape=mxgraph.cisco19.rect;prIcon=l2_switch;fillColor=#FAFAFA;strokeColor=#005073;html=1;fontSize=8;",
                    "width": "50",
                    "height": "50",
                }
            case DeviceRole.access_switch:
                return {
                    "style": "shape=mxgraph.cisco19.rect;prIcon=l2_switch;fillColor=#FAFAFA;strokeColor=#005073;html=1;fontSize=6;",
                    "width": "25",
                    "height": "25",
                }
            case DeviceRole.internet_switch:
                return {
                    "style": "shape=mxgraph.cisco19.rect;prIcon=l2_switch;fillColor=#FAFAFA;strokeColor=#005073;html=1;fontSize=8;",
                    "width": "50",
                    "height": "50",
                }
            case DeviceRole.firewall:
                return {
                    "style": "shape=mxgraph.cisco19.rect;prIcon=firewall;fillColor=#FAFAFA;strokeColor=#005073;html=1;fontSize=10;",
                    "width": "64",
                    "height": "50",
                }
            case DeviceRole.sdwan_hub:
                return {
                    "style": "shape=mxgraph.cisco19.rect;prIcon=server;fillColor=#FAFAFA;strokeColor=#005073;html=1;fontSize=8;",
                    "width": "64",
                    "height": "50",
                }
            case DeviceRole.wlan_ac:
                return {
                    "style": "shape=mxgraph.cisco19.rect;prIcon=wireless_lan_controller;fillColor=#FAFAFA;strokeColor=#005073;html=1;fontSize=8;",
                    "width": "64",
                    "height": "50",
                }
            case DeviceRole.wlan_ap:
                return {
                    "style": "shape=mxgraph.cisco19.rect;prIcon=wireless_access_point;fillColor=#FAFAFA;strokeColor=#005073;html=1;fontSize=6;",
                    "width": "16",
                    "height": "12.5",
                }
            case _:
                return {
                    "style": "shape=mxgraph.cisco19.rect;prIcon=server;fillColor=#FAFAFA;strokeColor=#005073;html=1;fontSize=8;",
                    "width": "25",
                    "height": "25",
                }


def enable_if_netflow_export(
    local_role: DeviceRole, remote_role: DeviceRole, port_channel: bool
) -> bool:
    if local_role == DeviceRole.core_switch and remote_role == DeviceRole.firewall:
        if port_channel:
            return False
        return True
    return False


def get_up_link_device_role(
    device_role: DeviceRole, all_device_roles: list[DeviceRole]
) -> DeviceRole | None:
    if device_role == DeviceRole.core_switch:
        if DeviceRole.firewall in all_device_roles:
            return DeviceRole.firewall
        return None
    if device_role in (DeviceRole.firewall, DeviceRole.wan_router):
        if DeviceRole.internet_switch in all_device_roles:
            return DeviceRole.internet_switch
        return None
    if device_role == DeviceRole.wlan_ac:
        if DeviceRole.core_switch in all_device_roles:
            return DeviceRole.core_switch
        return None
    if device_role == DeviceRole.distributed_switch:
        if DeviceRole.core_switch in all_device_roles:
            return DeviceRole.core_switch
        return None
    if device_role == DeviceRole.access_switch:
        if DeviceRole.distributed_switch in all_device_roles:
            return DeviceRole.distributed_switch
        if DeviceRole.core_switch in all_device_roles:
            return DeviceRole.core_switch
        if DeviceRole.firewall in all_device_roles:
            return DeviceRole.firewall
        return None
    if device_role == DeviceRole.internet_switch:
        return None
    return None


def enable_if_dhcp_snooping_trust(
    local_device_role: DeviceRole, remote_device_role: DeviceRole
) -> bool:
    if remote_device_role == DeviceRole.core_switch and local_device_role in {
        DeviceRole.access_switch,
        DeviceRole.distributed_switch,
    }:
        return True
    return bool(
        remote_device_role == DeviceRole.distributed_switch
        and local_device_role == DeviceRole.access_switch
    )


def enable_if_port_fast(device_role: DeviceRole, if_mode: IfMode) -> bool:
    return bool(device_role == DeviceRole.access_switch and if_mode == "access")


def enable_if_dhcp_snooping(device_role: DeviceRole, if_mode: IfMode) -> bool:
    """only for huawei platform"""
    return bool(device_role == DeviceRole.access_switch and if_mode == "access")


def generate_if_mode(local_role: DeviceRole, remote_role: DeviceRole) -> IfMode:
    if local_role == DeviceRole.core_switch:
        if remote_role in {
            DeviceRole.access_switch,
            DeviceRole.distributed_switch,
            DeviceRole.wlan_ac,
        }:
            return "trunk"
        elif remote_role in {
            DeviceRole.firewall,
            DeviceRole.wlan_ap,
            DeviceRole.internet_switch,
        }:
            return "access"
    elif local_role == DeviceRole.access_switch:
        if remote_role in {
            DeviceRole.core_switch,
            DeviceRole.distributed_switch,
            DeviceRole.wlan_ac,
        }:
            return "trunk"
        elif remote_role in {DeviceRole.firewall, DeviceRole.wlan_ap}:
            return "access"
        elif remote_role in {DeviceRole.firewall, DeviceRole.wlan_ap}:
            return "access"
    elif local_role in {DeviceRole.distributed_switch, DeviceRole.wlan_ac}:
        return "trunk"
    elif local_role == DeviceRole.internet_switch:
        if remote_role == DeviceRole.firewall:
            return "trunk"
        else:
            return "access"
    return "access"
