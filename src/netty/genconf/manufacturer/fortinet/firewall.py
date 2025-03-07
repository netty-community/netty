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

from typing import ClassVar
from pathlib import Path


from netty.genconf.factory.firewall_factory import FirewallFactory
from netty.consts import PROJECT_DIR


class FortinetFirewall(FirewallFactory):
    default_jinja_template_path: ClassVar[Path] = Path(
        f"{PROJECT_DIR}/src/netty/genconf/manufacturer/fortinet/"
    )
    default_jinja_template_name: ClassVar[str] = "firewall.j2"


    def get_lan_ports(self)->list[str]:
        ...
    
    def get_ha_ports(self)->list[str]:
        ...
    
        
    

    