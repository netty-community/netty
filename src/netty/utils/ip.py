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

import ipaddress


def netmask_to_wildcard_mask(netmask: str) -> str:
    """Convert a netmask to a wildcard mask."""
    netmask_int = int(ipaddress.IPv4Address(netmask))
    inverted_mask_int = ~netmask_int & 0xFFFFFFFF
    wildcard_mask = ipaddress.IPv4Address(inverted_mask_int)
    return str(wildcard_mask)


def wildcard_mask_to_netmask(wildcard_mask: str) -> str:
    """
    Convert a wildcard mask to a netmask.
    """
    wildcard_mask_int = int(ipaddress.IPv4Address(wildcard_mask))
    inverted_mask_int = ~wildcard_mask_int & 0xFFFFFFFF
    return str(ipaddress.IPv4Address(inverted_mask_int))


def find_excluded_ranges(
    network: ipaddress.IPv4Network,
    start: ipaddress.IPv4Address,
    end: ipaddress.IPv4Address,
) -> list[tuple[ipaddress.IPv4Address, ipaddress.IPv4Address]]:
    """
    Find all the excluded ranges in the network.
    """
    if start not in network:
        raise ValueError(f"Start address {start} is not in the network")
    if end not in network:
        raise ValueError(f"End address {end} is not in the network")
    if start > end:
        end, start = start, end

    all_addresses = list(network.hosts())
    start_index = all_addresses.index(start)
    end_index = all_addresses.index(end) + 1
    exclued_subnets = []
    if start_index > 0:
        exclued_subnets.append((all_addresses[0], all_addresses[start_index - 1]))
    if end_index < len(all_addresses):
        exclued_subnets.append((all_addresses[end_index], all_addresses[-1]))
    return exclued_subnets
