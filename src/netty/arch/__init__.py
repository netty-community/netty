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

from .device_role import (
    DeviceRole,
    get_up_link_device_role,
    enable_if_netflow_export,
    enable_if_dhcp_snooping,
    enable_if_dhcp_snooping_trust,
    enable_if_port_fast,
    generate_if_mode,
)
from .device_type import (
    DeviceType,
    InterfaceType,
    interface_type_mapping,
    ProductFamily,
)
from .platform import Manufacturer, Platform

__all__ = [
    "DeviceRole",
    "get_up_link_device_role",
    "enable_if_netflow_export",
    "enable_if_dhcp_snooping",
    "enable_if_dhcp_snooping_trust",
    "enable_if_port_fast",
    "generate_if_mode",
    "DeviceType",
    "ProductFamily",
    "InterfaceType",
    "interface_type_mapping",
    "Manufacturer",
    "Platform",
]
