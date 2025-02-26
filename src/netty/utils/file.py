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


from jinja2 import Environment, FileSystemLoader, Template


def load_jinja2_template(template_path: Path, template: str) -> Template:
    env = Environment(
        loader=FileSystemLoader(template_path),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    j2_template = env.get_template(template)
    return j2_template


def get_all_device_types(path: Path) -> list[str]:
    file_list = []
    for file in Path(path).rglob('*'): 
        if file.is_file() and file.suffix in ('.yaml', '.yml'):
            file_list.append(file.name.split('.')[0]) 

    return file_list
