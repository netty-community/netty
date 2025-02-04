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

from pydantic import IPvAnyAddress

from netty.project import Device, Connection, StackPort
from netty.arch import DeviceRole
from netty._types import FirewallWanHAMode
from netty.utils.netif import (
    interfaces_have_same_sub_port_number,
    process_interface_name,
)


def generate_default_gateway(
    devices: list[Device], device: Device
) -> IPvAnyAddress | None:
    switch_gateway = None
    fw_gateway = None
    for _device in devices:
        if _device.device_role == DeviceRole.firewall:
            fw_gateway = _device.management_ip.ip
        if _device.device_role == DeviceRole.core_switch:
            switch_gateway = _device.management_ip.ip
    if device.device_role in {
        DeviceRole.access_switch,
        DeviceRole.distributed_switch,
        DeviceRole.wlan_ac,
        DeviceRole.internet_switch,
    }:
        return switch_gateway
    if device.device_role == DeviceRole.firewall:
        return fw_gateway
    return None


def __sort_devices(devices: list[Device]) -> list[Device]:
    """
    sort devices by hostname
    """
    return sorted(devices, key=lambda x: x.hostname)


def remove_duplicate_devices(devices: list[Device]) -> list[Device]:
    """
    Remove duplicate devices by management_ip and hostname, when management_ip is the same, stacked is set to True
    """
    sorted_devices = __sort_devices(devices)
    management_ip_mapping: dict[IPvAnyAddress, Device] = {}
    unique_devices: list[Device] = []
    for device in sorted_devices:
        if device.management_ip not in management_ip_mapping:
            management_ip_mapping[device.management_ip] = device
            unique_devices.append(device)
    return unique_devices


def remove_stack_ports(
    devices: list[Device], connections: list[Connection]
) -> tuple[list[Connection], list[Device]]:
    result = []
    devices = __sort_devices(devices)
    device_hostname_mapping = {device.hostname: device for device in devices}
    for conn in connections:
        local_device = device_hostname_mapping.get(conn.local_hostname)
        remote_device = device_hostname_mapping.get(conn.remote_hostname)
        if (
            local_device
            and remote_device
            and local_device.management_ip == remote_device.management_ip
            and "switch" in local_device.device_role.lower()
        ):  
            if not local_device.stack_port:
                local_device.stack_port = StackPort(mad_ports=[], stack_ports=[])
            if not remote_device.stack_port:
                remote_device.stack_port = StackPort(mad_ports=[], stack_ports=[])
            if interfaces_have_same_sub_port_number(
                conn.local_interface_name, conn.remote_interface_name
            ):
                local_device.stack_port.mad_ports.extend([
                    process_interface_name(conn.local_interface_name, 1),
                    process_interface_name(conn.remote_interface_name, 2),
                ])
                remote_device.stack_port.mad_ports.extend([
                    process_interface_name(conn.local_interface_name, 1),
                    process_interface_name(conn.remote_interface_name, 2),
                ])
            else:
                local_device.stack_port.stack_ports = [
                    conn.local_interface_name,
                    conn.remote_interface_name
                ]
                remote_device.stack_port.stack_ports = [
                    conn.local_interface_name,
                    conn.remote_interface_name
                ]
        else:
            result.append(conn)
    return result, devices


def firewall_working_mode(devices: list[Device]) -> FirewallWanHAMode:
    firewall_numbers = 0
    int_sw_numbers = 0
    for device in devices:
        if device.device_role == DeviceRole.firewall:
            firewall_numbers += 1
        elif device.device_role == DeviceRole.internet_switch:
            int_sw_numbers += 1
    if firewall_numbers == 1:
        return "single-node"
    elif firewall_numbers >= 2:
        if int_sw_numbers == 0:
            return "enhance_ha_trunk_mode"
        if int_sw_numbers >= 1:
            return "internet_switch_ha_mode"
    return "enhance_ha_trunk_mode"
