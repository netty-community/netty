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

import re


class MacAddress:
    def __init__(self, mac: str) -> None:
        self.mac = mac_address_validator(mac)

    @property
    def cisco_format(self) -> str:
        self.mac.replace(":", "")
        return ".".join(self.mac[i : i + 4] for i in range(0, len(self.mac), 4)).lower()

    @property
    def ruijie_format(self) -> str:
        return self.cisco_format

    @property
    def huawei_format(self) -> str:
        self.mac.replace("-", "")
        return ".".join(self.mac[i : i + 4] for i in range(0, len(self.mac), 4)).lower()


def mac_address_validator(mac: str) -> str:
    """validate a single mac address and return `ietf-yang-types` mac format with lower case `xx:xx:xx:xx:xx:xx`.
    Please notice that every mac address write to db should follow this format.
    see: https://github.com/YangModels/yang/blob/main/vendor/cisco/xe/1661/ietf-yang-types.yang
    ```
    typedef mac-address {
    type string {
    pattern '[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}';
    }
    description
    "The mac-address type represents an IEEE 802 MAC address.
    The canonical representation uses lowercase characters.
    In the value set and its semantics, this type is equivalent
    to the MacAddress textual convention of the SMIv2.";
    reference
    "IEEE 802: IEEE Standard for Local and Metropolitan Area
                Networks: Overview and Architecture
    RFC 2579: Textual Conventions for SMIv2";
    }
    ```
    """
    _mac_address_regex = r"^[0-9a-fA-F]{12}$"
    mac_addr_len = 12
    input_mac = re.sub(r"[^0-9a-fA-F]", "", mac)
    if len(input_mac) != mac_addr_len:
        raise ValueError("validation_error.bad_mac_format")
    if re.match(_mac_address_regex, input_mac):
        return ":".join(
            input_mac[i : i + 2] for i in range(0, len(input_mac), 2)
        ).lower()
    raise ValueError("validation_error.bad_mac_format")
