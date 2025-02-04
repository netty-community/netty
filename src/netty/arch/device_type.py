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

from pydantic import BaseModel, Field, PositiveInt

from netty.arch.platform import Platform


class InterfaceType(StrEnum):
    base_1000_t = "1000base-t"
    base_10g_t = "10gbase-t"
    base_1000_x_sfp = "1000base-x-sfp"
    base_10g_x_sfpp = "10gbase-x-sfpp"
    base_10g_x_xfp = "10gbase-x-xfp"
    base_25g_x_sfp28 = "25gbase-x-sfp28"
    base_40g_x_qsfpp = "40gbase-x-qsfpp"
    base_100g_x_qspf28 = "100gbase-x-qsfp28"
    base_stack_port = "base_stack_port"

    @property
    def interface_type_color(self) -> str:
        mappings = {
            InterfaceType.base_1000_t: "#6cc0e5",
            InterfaceType.base_10g_t: "#6cc0e5",
            InterfaceType.base_1000_x_sfp: "#fbc93d",
            InterfaceType.base_10g_x_sfpp: "#fbc93d",
            InterfaceType.base_10g_x_xfp: "#fbc93d",
            InterfaceType.base_25g_x_sfp28: "#fbc93d",
            InterfaceType.base_40g_x_qsfpp: "#fbc93d",
            InterfaceType.base_100g_x_qspf28: "#fbc93d",
            InterfaceType.base_stack_port: "#00FF00",
        }
        if self not in mappings:
            msg = f"Invalid interface type, InterfaceType {self} is not defined"
            raise ValueError(msg)
        return mappings[self]


class _Interface(BaseModel):
    name: str
    type: InterfaceType


class ProductFamily(StrEnum):
    router = "router"
    switch = "switch"
    firewall = "firewall"
    wlc = "wlc"
    ap = "ap"


class DeviceType(BaseModel):
    platform: Platform
    name: str
    u_height: PositiveInt
    interfaces: list[_Interface]
    oob_interface: str | None = Field(default=None)
    stack_interfaces: list[str] | None = Field(default=None)
    uplink_interfaces: list[str] | None = Field(default=None)
    mad_interface: str | None = Field(default=None)
    ha_ports: list[str] | None = Field(default=None)
    lan_ports: list[str] | None = Field(default=None)
    enhance_ha_port: str | None = Field(default=None)
    power_consumption: int | None = Field(default=None, description="unit: W")
    poe_support: bool = Field(default=False)
    product_family: ProductFamily = Field(...)

    @property
    def interface_set(self) -> set[str]:
        return {interface.name for interface in self.interfaces}


def interface_type_mapping(if_type: str) -> InterfaceType:
    mappings = {
        "10G多模光纤": InterfaceType.base_10g_x_sfpp,
        "1G多模光纤": InterfaceType.base_1000_x_sfp,
        "CAT6E网线": InterfaceType.base_1000_t,
        "堆叠线": InterfaceType.base_stack_port,
        "10G单模光纤": InterfaceType.base_10g_x_sfpp,
        "1G单模光纤": InterfaceType.base_1000_x_sfp,
        "40G多模光纤": InterfaceType.base_40g_x_qsfpp,
        "40G单模光纤": InterfaceType.base_40g_x_qsfpp,
        "100G单模光纤": InterfaceType.base_100g_x_qspf28,
        "100G多模光纤": InterfaceType.base_100g_x_qspf28,
        "10G MM Fiber": InterfaceType.base_10g_x_sfpp,
        "1G MM Fiber": InterfaceType.base_1000_x_sfp,
        "CAT6E Cable": InterfaceType.base_1000_t,
        "Stack Cable": InterfaceType.base_stack_port,
        "10G SM Fiber": InterfaceType.base_10g_x_sfpp,
        "1G SM Fiber": InterfaceType.base_1000_x_sfp,
        "40G MM Fiber": InterfaceType.base_40g_x_qsfpp,
        "40G SM Fiber": InterfaceType.base_40g_x_qsfpp,
        "100G MM Fiber": InterfaceType.base_100g_x_qspf28,
    }
    if if_type not in mappings:
        msg = f"Invalid interface type, InterfaceType {if_type} is not defined"
        raise ValueError(msg)
    return mappings[if_type]
