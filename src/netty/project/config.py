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

from ipaddress import IPv4Address, IPv4Network
from pydantic import BaseModel, Field
from pydantic_extra_types.timezone_name import TimeZoneName
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)
from netty._types import AAAProtocol
from netty.consts import PROJECT_DIR, PROJECT_CONFIG


class Settings(BaseSettings):
    baseline_config: "BaselineConfig" = Field(
        ..., description="The baseline config of the network device"
    )
    system_config: "SystemConfig" = Field(
        ..., description="The system config of the network device"
    )
    snmp_config: "SnmpConfig" = Field(
        ..., description="The snmp config of the network device"
    )
    netflow_config: "NetflowConfig" = Field(
        ..., description="The netflow config of the network device"
    )
    aaa_config: "AAAConfig | None" = Field(..., description="dot1x authentication")

    model_config = SettingsConfigDict(
        yaml_file=f"{PROJECT_DIR}/projects/{PROJECT_CONFIG.corp_name}/{PROJECT_CONFIG.site_code}/config.yaml",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        env_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        dotenv_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        file_secret_settings: PydanticBaseSettingsSource,  # noqa: ARG003
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


class BaselineConfig(BaseModel):
    ssh_source_address: list[IPv4Network] | None = Field(
        default=None,
        description="The source network address can access ssh, default is all",
    )
    enable_ipv6: bool = Field(
        default=False, description="Whether to enable ipv6, disable by default"
    )
    enable_netflow: bool = Field(
        default=True,
        description="Whether to enable netflow/sflow/netstream, enable by default",
    )
    default_banner: str = Field(
        default=(
            "------------------------------------------------------------------------------------------------------\n"
            "Welcome to login Network Device\n"
            "This is a private property facility to be accessed by authorized users for internal systems.\n"
            "Unauthorized access is strictly prohibited.\n"
            "-------------------------------------------------------------------------------------------------------\n"
        )
    )
    errdisable_recovery_interval: int = Field(
        default=300,
        description="The interval of errdisable recovery, default is 300 seconds",
    )


class SystemConfig(BaseModel):
    management_username: str = Field(
        ..., description="The username of the local management user"
    )
    management_password: str = Field(
        ..., description="The password of the local management user"
    )
    management_vlan: int = Field(
        default=30, description="The vlan of the local management vlan"
    )
    default_timezone: TimeZoneName = Field(
        default="Asia/Shanghai", description="The default timezone of the device"
    )  # type: ignore
    ntp_server: list[IPv4Address] = Field(description="The ntp server of the device")
    dns_server: list[IPv4Address] = Field(description="The dns server of the device")
    syslog_server: IPv4Address | None = Field(
        default=None, description="The syslog server of the device"
    )
    syslog_udp_port: int = Field(
        default=514, description="The syslog udp port of the device"
    )
    firewall_manager: IPv4Address = Field(
        default=IPv4Address("0.0.0.0"),  # noqa: S104
        description="The firewall manager of the device, like fortimanager for fortinet and panoroma for PaloAlto",
    )


class SnmpConfig(BaseModel):
    snmp_community: str = Field(
        default="public", description="The community of the snmp, default is public"
    )
    snmp_port: int = Field(
        default=161, description="The port of the snmp, default is 161"
    )
    snmp_source: list[IPv4Network] | None = Field(
        default=None,
        description="The source network address can access snmp, default is all",
    )


class NetflowConfig(BaseModel):
    flow_export_address: IPv4Address | None = Field(
        default=None, description="The flow export address of the device"
    )
    flow_sample_rate: int = Field(
        default=4096, description="The flow sample rate of the device"
    )
    sflow_default_port: int = Field(
        default=6343, description="The default port of the sflow"
    )
    netflow_default_port: int = Field(
        default=2055, description="The default port of the netflow"
    )
    netstream_default_port: int = Field(
        default=2055, description="The default port of the netstream"
    )


class AAAConfig(BaseModel):
    aaa_protocol: AAAProtocol
    servers: list[IPv4Address]
    auth_port: int = Field(default=1812)
    acct_port: int = Field(default=1813)
    username: str | None = Field(default=None, description="aaa test username")
    password: str = Field(description="the auth/acct key")
    auth_vlan: int = Field(default=200)
    escape_vlan: int = Field(default=300)


settings = Settings()  # type: ignore
