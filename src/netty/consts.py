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

from pathlib import Path
from enum import StrEnum

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

PROJECT_DIR = Path(__file__).parent.parent.parent


class TemplateName(StrEnum):
    xlsx_file = "NetworkDesign.xlsx"
    hardware_sheet = "Hardware Devices"
    connection_sheet = "Device InterConnections"
    subnet_sheet = "Subnets"
    fix_ip_sheet = "Fixed IP Addresses"

class ProjectConfig(BaseSettings):
    corp_name: str = Field(default="the corp name of project")
    site_code: str = Field(default="the site_code of project")
    country_code: str = Field(default="CN")

    # customise the jinja2 template can be supported by config

    model_config = SettingsConfigDict(
        yaml_file=f"{PROJECT_DIR}/project.config.yaml", extra="ignore"
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


PROJECT_CONFIG = ProjectConfig()

DEFAULT_PROJECT_DIR = f"{PROJECT_DIR}/projects/{PROJECT_CONFIG.corp_name}/{PROJECT_CONFIG.site_code}"
DEFAULT_NETWORK_TEMPLATE_PATH = f"{PROJECT_DIR}/projects/{PROJECT_CONFIG.corp_name}/{PROJECT_CONFIG.site_code}/{TemplateName.xlsx_file}"
DEFAULT_PROJECT_INFO_PATH = f"{PROJECT_DIR}/projects/{PROJECT_CONFIG.corp_name}/{PROJECT_CONFIG.site_code}/project.yaml"
DEFAULT_TOPOLOGY_PATH = f"{PROJECT_DIR}/projects/{PROJECT_CONFIG.corp_name}/{PROJECT_CONFIG.site_code}/topology.drawio"
DEFAULT_CONFIG_OUTPUT_PATH = f"{PROJECT_DIR}//projects/{PROJECT_CONFIG.corp_name}/{PROJECT_CONFIG.site_code}/configuration"


