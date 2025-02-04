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

from typing import Literal

type IfMode = Literal["access", "trunk", "routed"]
type SnmpVersion = Literal["v2c", "v3"]
type Snmpv3SecurityLevel = Literal["noAuthNoPriv", "authNoPriv", "authPriv"]
type Snmpv3AuthProtocol = Literal[
    "NoAuth", "MD5", "SHA", "SHA224", "SHA256", "SHA384", "SHA512"
]
type Snmpv3PrivProtocol = Literal[
    "NoPriv", "DES", "AES", "AES192", "AES256", "AES192C", "AES256C"
]
type AAAProtocol = Literal["radius", "tacacs"]
type FlowType = Literal["netflow", "sflow", "netstream", None]
type FirewallWanHAMode = Literal["enhance_ha_trunk_mode", "internet_switch_ha_mode", "single-node"]
