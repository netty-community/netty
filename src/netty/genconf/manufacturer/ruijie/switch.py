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

from jinja2 import Template

from netty.genconf.factory.switch_factory import Switch, SwitchFactory, Stp
from netty.utils.mac import MacAddress
from netty.utils.file import load_jinja2_template
from netty.consts import PROJECT_DIR


class RuijieSwitch(SwitchFactory):
    default_jinja_template_path: ClassVar[Path] = Path(
        f"{PROJECT_DIR}/src/netty/genconf/manufacturer/ruijie/"
    )
    default_jinja_template_name: ClassVar[str] = "switch.j2"

    def enrich_data(self) -> Switch:
        pools = self.get_dhcp_pool_list()
        stp_role, stp_pri = self.device.device_role.stp_root
        for pool in pools:
            if not pool.fixed_ips:
                continue
            for ip in pool.fixed_ips:
                ip.mac_address = MacAddress(ip.mac_address).ruijie_format

        vlans = self.get_vlan_list()
        vlan_ifs = self.get_vlan_if_list()
        port_channels = self.get_port_channel_list()
        l3_ifs = self.get_l3_interface_list()

        return Switch(
            hostname=self.device.hostname,
            site_code=self.site_code,
            baseline_config=self.baseline_config,
            snmp_config=self.snmp_config,
            system_config=self.system_config,
            netflow_config=self.netflow_config,
            enable_guest_acl=self.device.device_role.enable_guest_acl,
            enable_stack=self.device.stacked,
            stack_config=self.device.stack_port,
            dhcp_pools=pools,
            aaa_config=self.aaa_config,
            stp_config=Stp(stp_root=stp_role, stp_priority=stp_pri),
            vlans=vlans,
            vlan_ifs=vlan_ifs,
            port_channels=port_channels,
            default_gateway=self.device.default_gateway,
            physical_ifs=self.device.interfaces,
            routed_ifs=l3_ifs,
        )

    def load_jinja2_template(self) -> Template:
        return load_jinja2_template(
            self.default_jinja_template_path, self.default_jinja_template_name
        )

    def generate_config(self) -> str:
        switch = self.enrich_data()
        template = self.load_jinja2_template()
        return template.render(switch=switch)
