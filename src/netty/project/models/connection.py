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

from pydantic import BaseModel, Field, PositiveInt, model_validator, computed_field

from netty.arch import InterfaceType, interface_type_mapping


type IfMode = Literal["access", "trunk"]


class Connection(BaseModel):
    local_hostname: str = Field(alias="LocalHostname")
    local_interface_name: str = Field(alias="LocalInterfaceName")
    if_type: InterfaceType = Field(
        default=InterfaceType.base_1000_t, alias="InterfaceType"
    )
    local_port_channel_id: PositiveInt | str | None = Field(
        default=None, alias="LocalPortChannelId"
    )
    remote_hostname: str = Field(alias="RemoteHostname")
    remote_interface_name: str = Field(alias="RemoteInterfaceName")
    remote_port_channel_id: PositiveInt | str | None = Field(
        default=None, alias="RemotePortChannelId"
    )

    @model_validator(mode="before")
    @classmethod
    def transform_if_type(cls, values: dict) -> dict:
        values["InterfaceType"] = interface_type_mapping(values["InterfaceType"])
        return values

    @computed_field
    @property
    def local_if_descr(self) -> str:
        return f"to_{self.remote_hostname}_{self.remote_interface_name}".replace(
            " ", ""
        )

    @computed_field
    @property
    def remote_if_descr(self) -> str:
        return f"to_{self.local_hostname}_{self.local_interface_name}".replace(" ", "")

    @computed_field
    @property
    def local_port_channel_descr(self) -> str:
        if self.remote_port_channel_id:
            return f"to_{self.remote_hostname}_{self.remote_port_channel_id}".replace(
                " ", ""
            )
        return ""

    @computed_field
    @property
    def remote_port_channel_descr(self) -> str:
        if self.local_port_channel_id:
            return f"to_{self.local_hostname}_{self.local_port_channel_id}".replace(
                " ", ""
            )
        return ""
