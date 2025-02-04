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

import logging
import csv

import typer
import yaml

from netty.consts import PROJECT_DIR
from netty.cli.default import (
    generate_default_config_yaml,
    generate_default_connection_headers,
    generate_default_device_headers,
    generate_default_fix_ip_headers,
    generate_default_subnet_headers,
    generate_project_yaml,
)

logger = logging.getLogger(__name__)


app = typer.Typer()



@app.command(help="create a new project, initial config files")
def new(
    corp_name: str,
    site_code: str,
    country_code: str,
    replace_project_config: bool = True,
) -> None:
    """Generate project.config.yaml if replace_project_config is True and initialize project in projects directory.
        corp_name: the corp name of project
        site_code: the site_code of project
        country_code: the country_code of project, default is CN, can be CN or US or any other country code
    """
    project_dir = PROJECT_DIR / "projects" / corp_name / site_code

    if replace_project_config:
        project_config = {
            "corp_name": corp_name,
            "site_code": site_code,
            "country_code": country_code,
        }
        with (PROJECT_DIR / "project.config.yaml").open("w", encoding="utf-8-sig") as f:
            yaml.safe_dump(project_config, f, indent=4, sort_keys=False)

    project_dir.mkdir(parents=True, exist_ok=True)

    files_to_create = {
        "project.yaml": generate_project_yaml(),
        "config.yaml": generate_default_config_yaml(country_code),
        "subnets.csv": generate_default_subnet_headers(),
        "fix_ips.csv": generate_default_fix_ip_headers(),
        "devices.csv": generate_default_device_headers(),
        "connections.csv": generate_default_connection_headers(),
    }

    for filename, content in files_to_create.items():
        file_path = project_dir / filename
        if not file_path.exists():
            with file_path.open("w", newline="", encoding="utf-8-sig") as f:
                if isinstance(content, list):
                    writer = csv.DictWriter(f, fieldnames=content)
                    writer.writeheader()
                else:
                    yaml.safe_dump(content, f, indent=4, sort_keys=False)

    configuration_dir = project_dir / "configuration"
    configuration_dir.mkdir(parents=True, exist_ok=True)


@app.command()
def version() -> None:
    import netty

    typer.echo(netty.__version__)


if __name__ == "__main__":
    app()
