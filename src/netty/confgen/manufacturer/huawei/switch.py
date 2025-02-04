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
from pydantic import IPvAnyAddress

from netty.confgen.factory.switch_factory import Switch, SwitchFactory, Stp, VlanIf
from netty.utils.mac import MacAddress
from netty.utils.file import load_jinja2_template
from netty.consts import PROJECT_DIR
from netty._types import FlowType


class HuaweiSwitch(SwitchFactory):
    default_jinja_template_path: ClassVar[Path] = Path(
        f"{PROJECT_DIR}/src/netty/confgen/manufacturer/huawei/"
    )
    default_jinja_template_name: ClassVar[str] = "switch.j2"

    def __flow_type(self) -> FlowType:
        lower_name = self.device.device_type.name.lower()
        if lower_name.startswith("s5700") or lower_name.startswith("s5700"):
            return "sflow"
        else:
            return "netstream"

    def __management_ip(self, vlan_ifs: list[VlanIf]) -> IPvAnyAddress | None:
        for vif in vlan_ifs:
            if vif.vlan_id == self.system_config.management_vlan:
                return vif.gateway
        return None

    def enrich_data(self) -> Switch:
        pools = self.get_dhcp_pool_list()
        stp_role, stp_pri = self.device.device_role.stp_root
        for pool in pools:
            if not pool.fixed_ips:
                continue
            for ip in pool.fixed_ips:
                ip.mac_address = MacAddress(ip.mac_address).huawei_format

        vlans = self.get_vlan_list()
        vlan_ifs = self.get_vlan_if_list()
        port_channels = self.get_port_channel_list()

        switch = Switch(
            hostname=self.device.hostname,
            site_code=self.site_code,
            baseline_config=self.baseline_config,
            snmp_config=self.snmp_config,
            system_config=self.system_config,
            netflow_config=self.netflow_config,
            stack_config=self.device.stack_port,
            enable_guest_acl=self.device.device_role.enable_guest_acl,
            enable_stack=self.device.stacked,
            dhcp_pools=pools,
            aaa_config=self.aaa_config,
            stp_config=Stp(stp_root=stp_role, stp_priority=stp_pri),
            vlans=vlans,
            vlan_ifs=vlan_ifs,
            port_channels=port_channels,
            default_gateway=self.device.default_gateway,
        )
        switch.flow_type = self.__flow_type()
        switch.management_ip = self.__management_ip(vlan_ifs)
        return switch

    def load_jinja2_template(self) -> Template:
        return load_jinja2_template(
            self.default_jinja_template_path, self.default_jinja_template_name
        )

    def generate_config(self) -> str:
        switch = self.enrich_data()
        template = self.load_jinja2_template()
        return template.render(switch=switch)
