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

from ipaddress import IPv4Network, IPv4Interface
from typing import NamedTuple


from netty.project import Subnet
from netty.consts import DEFAULT_PROJECT_DIR


class VlanSize(NamedTuple):
    vlan_id: int
    vlan_name: str
    subnet_size: int
    dhcp_pool: bool = False
    reserved_pool_addrs: int = 0


class Subnetter:
    def __init__(
        self,
        subnet: str,
        site_code: str,
        num_wired_endpoints: int,
        num_wireless_aps: int,
    ) -> None:
        self.subnet = IPv4Network(subnet)
        self.size = self.subnet.prefixlen
        self.site_code = site_code
        self.wired_endpoints = num_wired_endpoints
        self.wireless_aps = num_wireless_aps
        if self.size >= 22:
            raise ValueError("subnet too small, cannot automatically subneting")

    def template(self) -> list[VlanSize]:
        if self.size == 21:
            return [
                VlanSize(30, f"{self.site_code}-MGMT-30", 26, False, 0),
                VlanSize(600, f"{self.site_code}-APMGMT-600", 26, True, 0),
                VlanSize(60, f"{self.site_code}-Voice-60", 26, True, 10),
                VlanSize(70, f"{self.site_code}-Printer-70", 27, True, 10),
                VlanSize(3000, f"{self.site_code}-FWCONN-3000", 30, False, 0),
                VlanSize(90, f"{self.site_code}-Security-Monitor-90", 26, True, 10),
                VlanSize(110, f"{self.site_code}-Security-IOT-110", 26, True, 10),
                VlanSize(200, f"{self.site_code}-Wired-200", 24, True, 10),
                VlanSize(300, f"{self.site_code}-Guest-300", 24, True, 0),
                VlanSize(500, f"{self.site_code}-Server-500", 25, True, 20),
                VlanSize(800, f"{self.site_code}-Wireless-800", 23, True, 20),
            ]
        if self.size == 20:
            return [
                VlanSize(30, f"{self.site_code}-MGMT-30", 25, False, 0),
                VlanSize(600, f"{self.site_code}-APMGMT-600", 25, True, 0),
                VlanSize(60, f"{self.site_code}-Voice-60", 25, True, 10),
                VlanSize(70, f"{self.site_code}-Printer-70", 27, True, 10),
                VlanSize(3000, f"{self.site_code}-FWCONN-3000", 30, False, 0),
                VlanSize(90, f"{self.site_code}-Security-Monitor-90", 25, True, 10),
                VlanSize(110, f"{self.site_code}-Security-IOT-110", 25, True, 10),
                VlanSize(200, f"{self.site_code}-Wired-200", 24, True, 10),
                VlanSize(201, f"{self.site_code}-Wired-201", 24, True, 10),
                VlanSize(300, f"{self.site_code}-Guest-300", 24, True, 0),
                VlanSize(500, f"{self.site_code}-Server-500", 25, True, 20),
                VlanSize(800, f"{self.site_code}-Wireless-800", 22, True, 20),
            ]
        if self.size == 19:
            return [
                VlanSize(30, f"{self.site_code}-MGMT-30", 24, False, 0),
                VlanSize(3000, f"{self.site_code}-FWCONN-3000", 30, False, 0),
                VlanSize(600, f"{self.site_code}-APMGMT-600", 24, True, 0),
                VlanSize(60, f"{self.site_code}-Voice-60", 24, True, 10),
                VlanSize(70, f"{self.site_code}-Printer-70", 25, True, 10),
                VlanSize(90, f"{self.site_code}-Security-Monitor-90", 24, True, 10),
                VlanSize(110, f"{self.site_code}-Security-IOT-110", 24, True, 10),
                VlanSize(200, f"{self.site_code}-Wired-200", 23, True, 10),
                VlanSize(201, f"{self.site_code}-Wired-201", 23, True, 10),
                VlanSize(300, f"{self.site_code}-Guest-300", 23, True, 0),
                VlanSize(500, f"{self.site_code}-Server-500", 24, True, 20),
                VlanSize(800, f"{self.site_code}-Wireless-800", 22, True, 20),
                VlanSize(801, f"{self.site_code}-Wireless-801", 22, True, 20),
            ]
        if self.size == 18:
            return [
                VlanSize(30, f"{self.site_code}-MGMT-30", 24, False, 0),
                VlanSize(3000, f"{self.site_code}-FWCONN-3000", 30, False, 0),
                VlanSize(600, f"{self.site_code}-APMGMT-600", 24, True, 0),
                VlanSize(60, f"{self.site_code}-Voice-60", 24, True, 10),
                VlanSize(70, f"{self.site_code}-Printer-70", 25, True, 10),
                VlanSize(90, f"{self.site_code}-Security-Monitor-90", 24, True, 10),
                VlanSize(110, f"{self.site_code}-Security-IOT-110", 24, True, 10),
                VlanSize(200, f"{self.site_code}-Wired-200", 23, True, 10),
                VlanSize(201, f"{self.site_code}-Wired-201", 23, True, 10),
                VlanSize(202, f"{self.site_code}-Wired-202", 23, True, 10),
                VlanSize(203, f"{self.site_code}-Wired-203", 23, True, 10),
                VlanSize(204, f"{self.site_code}-Wired-204", 23, True, 10),
                VlanSize(300, f"{self.site_code}-Guest-300", 22, True, 0),
                VlanSize(500, f"{self.site_code}-Server-500", 24, True, 20),
                VlanSize(800, f"{self.site_code}-Wireless-800", 21, True, 20),
                VlanSize(801, f"{self.site_code}-Wireless-801", 21, True, 20),
            ]
        if self.size == 17:
            return [
                VlanSize(30, f"{self.site_code}-MGMT-30", 24, False, 0),
                VlanSize(3000, f"{self.site_code}-FWCONN-3000", 30, False, 0),
                VlanSize(600, f"{self.site_code}-APMGMT-600", 24, True, 0),
                VlanSize(601, f"{self.site_code}-APMGMT-601", 24, True, 0),
                VlanSize(60, f"{self.site_code}-Voice-60", 24, True, 10),
                VlanSize(70, f"{self.site_code}-Printer-70", 25, True, 10),
                VlanSize(90, f"{self.site_code}-Security-Monitor-90", 24, True, 10),
                VlanSize(110, f"{self.site_code}-Security-IOT-110", 24, True, 10),
                VlanSize(200, f"{self.site_code}-Wired-200", 23, True, 10),
                VlanSize(201, f"{self.site_code}-Wired-201", 23, True, 10),
                VlanSize(202, f"{self.site_code}-Wired-202", 23, True, 10),
                VlanSize(203, f"{self.site_code}-Wired-203", 23, True, 10),
                VlanSize(204, f"{self.site_code}-Wired-204", 23, True, 10),
                VlanSize(205, f"{self.site_code}-Wired-206", 23, True, 10),
                VlanSize(206, f"{self.site_code}-Wired-206", 23, True, 10),
                VlanSize(300, f"{self.site_code}-Guest-300", 22, True, 0),
                VlanSize(500, f"{self.site_code}-Server-500", 24, True, 20),
                VlanSize(800, f"{self.site_code}-Wireless-800", 21, True, 20),
                VlanSize(801, f"{self.site_code}-Wireless-801", 21, True, 20),
                VlanSize(802, f"{self.site_code}-Wireless-802", 21, True, 20),
            ]
        if self.size == 16:
            return [
                VlanSize(30, f"{self.site_code}-MGMT-30", 24, False, 0),
                VlanSize(30, f"{self.site_code}-MGMT-31", 24, False, 0),
                VlanSize(3000, f"{self.site_code}-FWCONN-3000", 30, False, 0),
                VlanSize(600, f"{self.site_code}-APMGMT-600", 24, True, 0),
                VlanSize(601, f"{self.site_code}-APMGMT-601", 24, True, 0),
                VlanSize(602, f"{self.site_code}-APMGMT-602", 24, True, 0),
                VlanSize(603, f"{self.site_code}-APMGMT-603", 24, True, 0),
                VlanSize(60, f"{self.site_code}-Voice-60", 24, True, 10),
                VlanSize(70, f"{self.site_code}-Printer-70", 24, True, 10),
                VlanSize(90, f"{self.site_code}-Security-Monitor-90", 24, True, 10),
                VlanSize(91, f"{self.site_code}-Security-Monitor-91", 24, True, 10),
                VlanSize(110, f"{self.site_code}-Security-IOT-110", 24, True, 10),
                VlanSize(111, f"{self.site_code}-Security-IOT-111", 24, True, 10),
                VlanSize(200, f"{self.site_code}-Wired-200", 23, True, 10),
                VlanSize(201, f"{self.site_code}-Wired-201", 23, True, 10),
                VlanSize(202, f"{self.site_code}-Wired-202", 23, True, 10),
                VlanSize(203, f"{self.site_code}-Wired-203", 23, True, 10),
                VlanSize(204, f"{self.site_code}-Wired-204", 23, True, 10),
                VlanSize(205, f"{self.site_code}-Wired-205", 23, True, 10),
                VlanSize(206, f"{self.site_code}-Wired-206", 23, True, 10),
                VlanSize(207, f"{self.site_code}-Wired-207", 23, True, 10),
                VlanSize(208, f"{self.site_code}-Wired-208", 23, True, 10),
                VlanSize(208, f"{self.site_code}-Wired-208", 23, True, 10),
                VlanSize(300, f"{self.site_code}-Guest-300", 22, True, 0),
                VlanSize(500, f"{self.site_code}-Server-500", 24, True, 20),
                VlanSize(800, f"{self.site_code}-Wireless-800", 21, True, 20),
                VlanSize(801, f"{self.site_code}-Wireless-801", 21, True, 20),
                VlanSize(802, f"{self.site_code}-Wireless-802", 21, True, 20),
            ]
        return []

    def allocate(self) -> list[Subnet]:
        current_network = self.subnet.network_address
        used_subnets = []
        results = []
        for vlan in self.template():
            subnet_size = IPv4Network(
                f"0.0.0.0/{vlan.subnet_size}", strict=False
            ).prefixlen
            subnet: IPv4Network
            while True:
                subnet = IPv4Network(
                    f"{str(current_network)}/{subnet_size}", strict=False
                )
                overlap = False
                for used_subnet in used_subnets:
                    if subnet.overlaps(used_subnet):
                        overlap = True
                        break
                if not overlap:
                    break
                current_network = subnet.broadcast_address + 1
            used_subnets.append(subnet)
            current_network = subnet.broadcast_address + 1
            results.append(
                Subnet(
                    VlanId=vlan.vlan_id,
                    VlanName=vlan.vlan_name,
                    dhcp_pool=vlan.dhcp_pool,
                    DHCPNetwork=subnet if vlan.dhcp_pool else None,
                    DHCPRangeStart=subnet.network_address + vlan.reserved_pool_addrs + 1
                    if vlan.dhcp_pool
                    else None,
                    DHCPRangeEnd=subnet.broadcast_address - 1
                    if vlan.dhcp_pool
                    else None,
                    IfAddress=IPv4Interface(
                        f"{subnet.network_address + 1}/{subnet.prefixlen}"
                    ),
                )
            )
        return results

    def to_csv(self):
        results = self.allocate()
        with open(f"{DEFAULT_PROJECT_DIR}/subnets.csv", "w") as f:
            f.write(
                "VlanId,VlanName,DHCPNetwork,DHCPPool,DHCPPoolRangeStart,DHCPPoolRangeEnd,IfAddress\n"
            )
            for r in results:
                dns = ",".join([i.compressed for i in r.dns_server])
                f.write(
                    f"{r.vlan_id},{r.name},{r.dhcp_network},{r.dhcp_pool},{dns},{r.dhcp_range_start},{r.dhcp_range_end},{r.if_addr}\n"
                )
