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

from netty.utils.net import get_default_dns_server, get_default_ntp_server


from netty.project import Subnet, Device, Connection, FixedIP


def generate_default_config_yaml(region: str):
    config = {
        "baseline_config": {
            "enable_ipv6": False,
            "enable_netflow": True,
            "errdisable_recovery_interval": 300,
            "default_banner": (
                "------------------------------------------------------------------------------------------------------\n"
                "Welcome to login Network Device\n"
                "This is a private property facility to be accessed by authorized users for internal systems.\n"
                "Unauthorized access is strictly prohibited.\n"
                "-------------------------------------------------------------------------------------------------------\n"
            ),
        },
        "system_config": {
            "management_username": "admin",
            "management_password": "change_me_password",
            "management_vlan": 30,
            "default_timezone": "Asia/Shanghai",
            "dns_server": [r.compressed for r in get_default_dns_server(region=region)],
            "ntp_server": [r.compressed for r in get_default_ntp_server(region=region)],
            "syslog_server": "",
            "syslog_udp_port": 514,
            "max_line_vty": 15,
            "firewall_manager": "101.126.153.88",
        },
        "snmp_config": {
            "snmp_version": "v2c",
            "snmp_community": "change_me_community",
            "snmp_port": 161,
            "snmp_source": [],
        },
        "netflow_config": {
            "flow_export_address": "10.1.0.250",
            "flow_sample_rate": 4096,
            "sflow_default_port": 6343,
            "netflow_default_port": 2055,
            "netstream_default_port": 2055,
        },
        "aaa_config": {
            "aaa_protocol": "radius",
            "servers": [],
            "auth_port": 1812,
            "acct_port": 1813,
            "username": "",
            "password": "",
            "auth_vlan": 200,
            "escape_vlan": 300,
        },
    }

    return config


def generate_default_subnet_headers() -> list[str]:
    fields = Subnet.model_fields.values()
    return [field.alias for field in fields if field.alias]


def generate_default_device_headers() -> list[str]:
    fields = Device.model_fields.values()
    return [field.alias for field in fields if field.alias]


def generate_default_connection_headers() -> list[str]:
    fields = Connection.model_fields.values()
    return [field.alias for field in fields if field.alias]


def generate_default_fix_ip_headers() -> list[str]:
    fields = FixedIP.model_fields.values()
    return [field.alias for field in fields if field.alias]


def generate_project_yaml() -> dict:
    project = {
        "lan_gateway": "192.168.1.253",
        "lan_networks": [
            {"network": "192.168.0.0/19", "enable_nat": True},
            {"network": "192.168.255.0/24", "enable_nat": False},
        ],
        "wan_networks": {
            "networks": [
                {
                    "provider": "CU",
                    "circuit_type": "Internet",
                    "bandwidth": 500,
                    "ip_address": "100.100.100.100/24",
                    "gateway": "100.100.100.1",
                    "port_name": "wan1",
                    "probe_icmp_ping_target": "223.5.5.5",
                },
                {
                    "provider": "CT",
                    "circuit_type": "ADSL",
                    "bandwidth": 1000,
                    "pppoe_username": "user",
                    "pppoe_password": "password",
                    "port_name": "wan2",
                    "probe_icmp_ping_target": "223.6.6.6",
                },
            ],
            "load_balance_mode": "active-active",
        },
    }

    return project
