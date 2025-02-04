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

import re


def process_interface_name(interface_name: str, slot_number: int) -> str:
    """
    Processes a network device interface name by inserting a slot number.

    :param interface_name: Original interface name (e.g., Gi0/1, Te0/2)
    :param slot_number: Slot number to insert (e.g., 1)
    :return: Processed interface name (e.g., Gi1/0/1, Te1/0/2)
    """
    if slot_number <= 0:
        raise ValueError("Slot number must be greater than 0")
    interface_pattern_with_slot = re.match(r"(\D+)(\d+)/(\d+)/(\d+)", interface_name)

    # 如果接口名称包含slot编号如 Gi1/0/1
    if interface_pattern_with_slot:
        interface_type, existing_slot, port, sub_port = (
            interface_pattern_with_slot.groups()
        )
        return f"{interface_type}{slot_number}/{port}/{sub_port}"

    # 定义一个正则表达式来匹配没有slot编号的接口名称如 Gi0/1, Te0/2
    interface_pattern_without_slot = re.match(r"(\D+)(\d+)/(\d+)", interface_name)

    # 如果接口名称没有slot编号如 Gi0/1
    if interface_pattern_without_slot:
        interface_type, port, sub_port = interface_pattern_without_slot.groups()
        return f"{interface_type}{slot_number}/{port}/{sub_port}"

    msg = f"Invalid interface name: {interface_name}"
    raise ValueError(msg)


def interfaces_have_same_sub_port_number(
    local_interface: str, remote_interface: str
) -> bool:
    """Checks if two interface names have the same sub-port number."""
    local_interface_match = re.match(r"(\D+)(\d+)/(\d+)/(\d+)", local_interface)
    remote_interface_match = re.match(r"(\D+)(\d+)/(\d+)/(\d+)", remote_interface)
    if local_interface_match and remote_interface_match:
        _, _, _, local_sub_port_number = local_interface_match.groups()
        _, _, _, remote_sub_port_number = remote_interface_match.groups()
        return local_sub_port_number == remote_sub_port_number

    local_interface_match = re.match(r"(\D+)(\d+)/(\d+)", local_interface)
    remote_interface_match = re.match(r"(\D+)(\d+)/(\d+)", remote_interface)
    if local_interface_match and remote_interface_match:
        _, _, local_sub_port_number = local_interface_match.groups()
        _, _, remote_sub_port_number = remote_interface_match.groups()
        return local_sub_port_number == remote_sub_port_number

    return False


def generate_port_channel_name(
    if_descr: str, port_channel_if_prefix: str
) -> str:
    if if_descr == "":
        return ""
    parts = if_descr.split("_")
    if len(parts) != 3:
        raise ValueError(
            f"invalid hostname: {if_descr}, hostname should not contain `_`"
        )
    return f"to_{parts[1]}_{port_channel_if_prefix}{parts[2]}"


def match_interface_by_port_id(port_list: set[str], port_id: int)->str:
    port_pattern = re.compile(r'(\d+)$')

    port_map = {}
    for port in port_list:
        match = port_pattern.search(port)
        if match:
            port_number = int(match.group(1))
            port_map[port_number] = port
    if port_id not in port_map:
        raise ValueError(f"port {port_id} not found in port list {port_list}")
    return port_map[port_id]

