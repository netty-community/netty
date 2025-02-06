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

from pydantic import (
    BaseModel,
    Field,
    IPvAnyAddress,
    IPvAnyInterface,
    IPvAnyNetwork,
    PositiveInt,
    model_validator,
)

from netty.utils.net import get_default_dns_server
from netty.consts import PROJECT_CONFIG

IPv4_VERSION = 4
IPv6_VERSION = 6


class Subnet(BaseModel):
    vlan_id: PositiveInt | None = Field(
        default=None, alias="VlanId", description="The vlan id of the subnet"
    )
    name: str | None = Field(
        ...,
        alias="VlanName",
        description="The vlan name/interface description of the subnet",
    )
    interface_name: str | None = Field(
        default=None, alias="InterfaceName", description="The interface name of the subnet"
    )
    if_addr: IPvAnyInterface = Field(
        ..., alias="IfAddress", description="The if_addr of the subnet"
    )
    vrf_name: str | None = Field(
        default=None, alias="VrfName", description="The vrf name of the subnet"
    )
    dhcp_pool: bool = Field(
        default=False,
        description="Whether to enable dhcp pool, disable by default",
    )
    dhcp_network: IPvAnyNetwork | None = Field(
        default=None, alias="DHCPNetwork", description="The network of the dhcp range"
    )
    dhcp_range_start: IPvAnyAddress | None = Field(
        default=None, alias="DHCPRangeStart", description="The start of the dhcp range"
    )
    dhcp_range_end: IPvAnyAddress | None = Field(
        default=None, alias="DHCPRangeEnd", description="The end of the dhcp range"
    )
    dns_server: list[IPvAnyAddress] = Field(
        default=[], alias="DNSServer", description="The domain name of the subnet"
    )

    @model_validator(mode="before")
    @classmethod
    def enrich_dns_server(cls, values: dict) -> dict:
        value = values.get("DNSServer")
        if value is None:
            values["DNSServer"] = get_default_dns_server(
                region=PROJECT_CONFIG.country_code
            )
        elif "," in value:
            values["DNSServer"] = value.split(",")
        elif " " in value:
            values["DNSServer"] = value.split(" ")
        return values

    @model_validator(mode="after")
    def validate_subnet(self) -> "Subnet":
        if not self.vlan_id and not self.interface_name:
            raise ValueError("VlanID or InterfaceName must be provided one of them")
        if self.vlan_id and self.interface_name:
            raise ValueError(
                "VlanId and InterfaceName cannot be provided at the same time"
            )
        if self.dhcp_network:
            self.dhcp_pool = True
            network_version = self.dhcp_network.version
            invalid_version_msg = (
                "The dhcp pool ip version is not the same as the network ip version"
            )

            def check_ip_version(ip: IPvAnyAddress) -> None:
                if ip.version != network_version:
                    raise ValueError(invalid_version_msg)

            if self.dhcp_range_start:
                check_ip_version(self.dhcp_range_start)
            if self.dhcp_range_end:
                check_ip_version(self.dhcp_range_end)
            check_ip_version(self.if_addr)
            for dns_server in self.dns_server:
                check_ip_version(dns_server)

            if (
                self.dhcp_range_start
                and self.dhcp_range_end
                and self.dhcp_range_start > self.dhcp_range_end  # type: ignore
            ):
                raise ValueError(
                    "The start of the dhcp pool must be less than the end of the dhcp pool"
                )
        if self.dhcp_pool and not self.dhcp_network:
            raise ValueError("dhcp_network must be provided when dhcp_pool is True")

        return self


class FixedIP(BaseModel):
    ip: IPvAnyInterface = Field(
        ..., description="The fixed ip with netmask", alias="IPAddress"
    )
    mac_address: str = Field(
        ..., description="The fixed mac address of the subnet", alias="MacAddress"
    )
    name: str = Field(..., description="The fixed ip name of the subnet", alias="Name")
