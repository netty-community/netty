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

import csv
from pathlib import Path
import logging
from collections import defaultdict

import yaml
from pydantic import IPvAnyAddress 
from netty.consts import (
    DEFAULT_DEVICES_PATH,
    DEFAULT_FIX_IPS_PATH,
    DEFAULT_CONNECTIONS_PATH,
    DEFAULT_PROJECT_INFO_PATH,
    DEFAULT_SUBNETS_PATH,
)
from netty.project import Device, Connection, FixedIP, Subnet, Project
from netty.utils.netif import match_interface_by_port_id, process_interface_name
from netty.arch import DeviceRole, InterfaceType

logger = logging.getLogger(__name__)

def parse_subnets(subnets_path: Path = Path(DEFAULT_SUBNETS_PATH)) -> list[Subnet]:
    """Parse the subnets configuration from the given path."""
    logging.info("[parse_subnets] Parsing subnets from %s", subnets_path)
    with subnets_path.open(encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        results= [
            Subnet.model_validate(
                {key: value if value else None for key, value in row.items()}
            )
            for row in reader
        ]
        logging.info(f"[parse_subnets] Done parsing subnets from {subnets_path}, got {len(results)} subnets")
        return results


def parse_devices(path: Path = Path(DEFAULT_DEVICES_PATH)) -> list[Device]:
    """Parse the devices configuration from the given path."""
    logging.info("[parse_devices] Parsing devices from %s", path)
    with Path.open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        results= [
            Device.model_validate(
                {key: value if value else None for key, value in row.items()}
            )
            for row in reader
        ]
        logging.info(f"[parse_devices] Done parsing devices from {path}, got {len(results)} devices")
        return results


def parse_connections(
    path: Path = Path(DEFAULT_CONNECTIONS_PATH),
) -> list[Connection]:
    logging.info("[parse_connections] Parsing connections from %s", path)
    with Path.open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        results= [
            Connection.model_validate(
                {key: value if value else None for key, value in row.items()}
            )
            for row in reader
        ]
        logging.info(f"[parse_connections] Done parsing connections from {path}, got {len(results)} connections")
        return results

def enrich_devices_and_connections(
    devices: list[Device], conns: list[Connection]
) -> tuple[list[Device], list[Connection]]:
    """TODO: enrich connections when local_interface_name and remote_interface name is integer by devicetype"""
    sorted_devices = sorted(devices, key=lambda x: x.hostname)
    management_ip_count:dict[IPvAnyAddress, int] = defaultdict(int)
    cluster: dict[IPvAnyAddress, list[Device]] = defaultdict(list)
    for device in sorted_devices:
        if device.device_role == DeviceRole.wlan_ap:
            continue
        management_ip_count[device.management_ip] += 1
    for device in sorted_devices:
        if management_ip_count[device.management_ip] > 1:
            device.stacked = True
            cluster[device.management_ip].append(device)
    hostname_device_mapping = {device.hostname: device for device in devices}
    for conn in conns:
        local_device = hostname_device_mapping.get(conn.local_hostname)
        remote_device = hostname_device_mapping.get(conn.remote_hostname)
        if local_device and conn.local_interface_name.isdigit():
            local_interface = match_interface_by_port_id(local_device.device_type.interface_set, int(conn.local_interface_name))
        else:
            local_interface = conn.local_interface_name
        if remote_device and conn.remote_interface_name.isdigit():
            remote_interface = match_interface_by_port_id(remote_device.device_type.interface_set, int(conn.remote_interface_name))
        else:
            remote_interface = conn.remote_interface_name
        if local_device and local_device.device_role not in (DeviceRole.firewall, DeviceRole.wlan_ap):
            if local_device.stacked and remote_device and local_device.management_ip == remote_device.management_ip:
                if conn.if_type == InterfaceType.base_stack_port:
                    conn.local_interface_name = local_interface
                    conn.remote_interface_name = remote_interface
                    continue
                else:
                    index = cluster[remote_device.management_ip].index(local_device)
                    if local_interface:
                        local_interface = process_interface_name(local_interface, index + 1)
            else:
                index = cluster[local_device.management_ip].index(local_device)
                if local_interface:
                    local_interface = process_interface_name(local_interface, index + 1) # type: ignore
            conn.local_interface_name = local_interface  # type: ignore
        if remote_device and remote_interface and remote_device.device_role not in (DeviceRole.firewall, DeviceRole.wlan_ap):
            if remote_device.stacked and local_device:
                index = cluster[remote_device.management_ip].index(remote_device)
                if remote_interface:
                    remote_interface = process_interface_name(remote_interface, index + 1) # type: ignore
            conn.remote_interface_name = remote_interface
    return sorted_devices, conns
            

def parse_project_info(path: Path = Path(DEFAULT_PROJECT_INFO_PATH)) -> Project:
    logging.info("[parse_project_info] Parsing project info from %s", path)
    with Path.open(path, encoding="utf-8-sig") as f:
        reader = yaml.safe_load(f)
        result = Project.model_validate(reader)
        logging.info(f"[parse_project_info] Done parsing project info from {path}")
        return result


def parse_fix_ips(path: Path = Path(DEFAULT_FIX_IPS_PATH)) -> list[FixedIP]:
    logging.info("[parse_fix_ips] Parsing fix ips from %s", path)
    with Path.open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        results = [FixedIP.model_validate(row) for row in reader]
        logging.info(f"[parse_fix_ips] Done parsing fix ips from {path}, got {len(results)} fix ips")
        return results
