"""Copyright 2024 wangxin.jeffry@gmail.com
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at.

http:www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    IPvAnyInterface,
    IPvAnyNetwork,
    PositiveInt,
    model_validator,
    IPvAnyAddress,
    computed_field
)

type CircuitType = Literal["Internet", "ADSL", "MPLS", "P2P"]
type LoadBalanceMode = Literal["active-passive", "active-active"]


class Project(BaseModel):
    lan_gateway: IPvAnyAddress
    lan_networks: list["LanNetwork"] = Field(..., description="The LAN block of the site")
    wan_networks: "WanNetwork" = Field(..., description="The WAN networks of the site")


class LanNetwork(BaseModel):
    network: IPvAnyNetwork
    enable_nat: bool = True


class WanNetwork(BaseModel):
    networks: list["WanNetworkConfig"]
    load_balance_mode: LoadBalanceMode = Field(
        default="active-active", description="The load balance mode of the WAN network"
    )

    @computed_field
    @property
    def wan_member_ports_str(self)->str:
        wan_str = ""
        for wan in self.networks:
            wan_str += f'"{wan.port_name}" '
        return wan_str
    



class WanNetworkConfig(BaseModel):
    provider: str = Field(..., description="The provider of the WAN network")
    circuit_type: CircuitType = Field(..., description="The type of the WAN network")
    bandwidth: PositiveInt = Field(..., description="The bandwidth of the WAN network")
    pppoe_username: str | None = Field(
        None, description="The username of the WAN network"
    )
    pppoe_password: str | None = Field(
        None, description="The password of the WAN network"
    )
    ip_address: IPvAnyInterface | None = Field(
        default=None,
        description="The ip_address of the WAN network config on the router/firewall",
    )
    port_name: str = Field(..., description="the interface name connect to wan network")
    gateway: IPvAnyAddress | None = Field(
        default=None, description="The gateway of the WAN network"
    )
    ecmp_weight: PositiveInt = Field(
        default=1,
        description="The ecmp weight of the WAN network, default is 1",
    )
    distance: PositiveInt = Field(
        default=10,
        description="The distance of route",
    )
    probe_icmp_ping_target: IPvAnyAddress | None = Field(
        default=None, description="sdwan health check target"
    )

    @model_validator(mode="after")
    def validate_data(self) -> "WanNetworkConfig":
        if self.circuit_type == "Internet":
            if not self.ip_address and not self.gateway:
                raise ValueError("Internet WAN network must have ip_address or gateway")
        if (
            self.circuit_type == "ADSL"
            and not self.pppoe_username
            and not self.pppoe_password
        ):
            raise ValueError(
                "ADSL WAN network must have pppoe_username and pppoe_password"
            )
        return self

