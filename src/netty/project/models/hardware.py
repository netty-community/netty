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

from functools import lru_cache


from pydantic import (
    BaseModel,
    Field,
    IPvAnyAddress,
    IPvAnyInterface,
    field_validator,
    model_validator,
    PositiveInt,
)
import yaml

from netty.arch import DeviceRole, DeviceType, Manufacturer
from netty._types import IfMode
from netty.consts import PROJECT_DIR


@lru_cache
def parse_device_type(manufacturer: Manufacturer, device_type: str) -> DeviceType:
    """
    Parse device type YAML file and return a DeviceType object.

    Args:
        manufacturer (Manufacturer): The manufacturer of the device.
        device_type (str): The model of the device.

    Returns:
        DeviceType: The parsed DeviceType object.
    """
    file_path = (
        PROJECT_DIR
        / "collections"
        / "devicetypes"
        / manufacturer
        / f"{device_type}.yaml"
    )
    if not file_path.exists():
        msg = f"Manufacturer: {manufacturer} Device type {device_type} not defined, need to be added to {file_path}"
        raise ValueError(msg)

    with file_path.open() as f:
        data = yaml.safe_load(f)
        return DeviceType.model_validate(data)


class Device(BaseModel):
    hostname: str = Field(alias="Hostname")
    management_ip: IPvAnyInterface = Field(alias="ManagementIP")
    manufacturer: str = Field(alias="Manufacturer")
    device_type: DeviceType = Field(alias="DeviceType")
    device_role: DeviceRole = Field(alias="DeviceRole")
    serial_number: str | None = Field(default=None, alias="SerialNumber")
    default_gateway: IPvAnyAddress | None = Field(default=None, alias="DefaultGateway")
    server_room: str | None = Field(default=None, alias="ServerRoom")
    stacked: bool = Field(default=False)
    interfaces: list["PhysicalInterface"] = Field(default=[])
    stack_port: "StackPort| None" = Field(default=None)

    @field_validator("management_ip", mode="before")
    @classmethod
    def convert_ip(cls, value: str) -> str:
        if value.lower() == "dhcp":
            return "0.0.0.0"  # noqa: S104
        return value

    @model_validator(mode="before")
    @classmethod
    def parse_device_type(cls, values: dict) -> dict:
        values["DeviceType"] = parse_device_type(
            Manufacturer(values["Manufacturer"]), values["DeviceType"]
        )
        return values


class PhysicalInterface(BaseModel):
    if_name: str
    if_mode: IfMode
    if_descr: str | None = None
    port_channel_descr: str | None = None
    if_addr: IPvAnyInterface | None = None
    vlan_id: int | None = None
    port_channel_id: PositiveInt | None = None
    dhcp_snooping_enable: bool = False
    dhcp_snooping_trust: bool = False
    enable_netflow: bool = False
    port_fast: bool = False
    vrf_name: str | None = None
    mtu: int | None = None


class StackPort(BaseModel):
    stack_ports: list[str]
    mad_ports: list[str]
