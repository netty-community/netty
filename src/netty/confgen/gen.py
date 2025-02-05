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

import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

from netty.arch import DeviceRole
from netty.topogen.diagram import Node, Link, Group
from netty.project import Device, Connection
from netty.consts import DEFAULT_TOPOLOGY_PATH, PROJECT_CONFIG


class TopoGen:
    def __init__(self, corp_name: str, site_code: str) -> None:
        self.mxfile = ET.Element(
            "mxfile",
            host="Electron",
            agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/25.0.2 Chrome/128.0.6613.186 Electron/32.2.5 Safari/537.36",
        )
        self.diagram = ET.SubElement(
            self.mxfile,
            "diagram",
            id="diagram-1",
            name=f"{corp_name.title()}-{site_code.title()}-Network Topology",
        )
        self.mxGraphModel = ET.SubElement(
            self.diagram,
            "mxGraphModel",
            grid="1",
            gridSize="10",
            guides="1",
            tooltips="1",
            connect="1",
            arrows="1",
            fold="1",
            page="1",
            pageScale="1",
            pageWidth="850",
            pageHeight="1100",
            math="0",
            shadow="0",
        )
        self.root = ET.SubElement(self.mxGraphModel, "root")
        self.mxCellId0 = ET.SubElement(self.root, "mxCell", id="0")
        self.mxCellId1 = ET.SubElement(self.root, "mxCell", id="1", parent="0")  # type: ignore

    def add_group(self, group: Group) -> None:
        self.root.append(group.to_xml())

    def add_groups(self, groups: list[Group]) -> None:
        self.root.extend([group.to_xml() for group in groups])

    def add_node(self, node: Node) -> None:
        self.root.append(node.to_xml())

    def add_nodes(self, nodes: list[Node]) -> None:
        self.root.extend([node.to_xml() for node in nodes])

    def add_link(self, link: Link) -> None:
        self.root.extend([link.to_link_xml(), link.to_link_label_xml()])

    def add_links(self, links: list[Link]) -> None:
        for link in links:
            self.add_link(link)

    def display_xml(self) -> bytes:
        return ET.tostring(self.mxfile)

    def export_xml(self, path: Path) -> None:
        with path.open("wb") as f:
            tree = ET.ElementTree(self.mxfile)
            tree.write(f)

    def __repr__(self) -> str:
        return str(self.display_xml())


def _lr_cord_calculator(count: int) -> dict[int, tuple[float, float, float, float]]:
    """calculate left-to-right line cord, tuple[exitX,exitY,entryX,entryY]"""
    coordinates = {}
    if count == 1:
        coordinates[1] = (1, 0.5, 0, 0.5)
    elif count == 2:
        coordinates[1] = (1, 0.25, 0, 0.25)
        coordinates[2] = (1, 0.75, 0, 0.75)
    elif count in (3, 4):
        for i in range(1, count + 1):
            coordinates[i] = (1, (i - 1) / (count - 1), 0, (i - 1) / (count - 1))
    elif count in (5, 6):
        for i in range(1, count + 1):
            coordinates[i] = (1, (i - 1) / (count - 1), 0, (i - 1) / (count - 1))
    return coordinates


def _td_cord_calculator(count: int) -> dict[int, tuple[float, float, float, float]]:
    """Calculate coordinates for top-down lines, tuple[exitX,exitY,entryX,entryY]"""
    if count == 1:
        return {1: (0.5, 1, 0.5, 0)}
    coordinates = {}
    for i in range(1, count + 1):
        coordinates[i] = (
            0.2 + (i - 1) / (count - 1) * 0.6,
            1,
            0.2 + (i - 1) / (count - 1) * 0.6,
            0,
        )
    return coordinates


def _dt_cord_calculator(count: int) -> dict[int, tuple[float, float, float, float]]:
    """Calculate coordinates for down-to-top lines, tuple[exitX,exitY,entryX,entryY]"""
    coordinates = {}
    if count == 1:
        coordinates[1] = (0.5, 0, 0.5, 1)
    elif count in (2, 3, 4):
        for i in range(1, count + 1):
            coordinates[i] = (
                0.2 + (i - 1) / (count - 1) * 0.6,
                0,
                0.2 + (i - 1) / (count - 1) * 0.6,
                1,
            )
    return coordinates


def _node_cord_calculator(
    nodes: list[Node], x_offset: int = 150, y_offset: int = 200
) -> list[Node]:
    level_dict = defaultdict(list)
    for node in nodes:
        level_dict[node.device_role.node_level].append(node)
    for level, level_nodes in level_dict.items():
        num_of_nodes = len(level_nodes)
        mid_point = (num_of_nodes - 1) // 2
        left_offset = 0
        right_offset = 0
        for i, node in enumerate(level_nodes):
            if i < mid_point:
                node.x = left_offset - x_offset * (mid_point - i)
            elif i > mid_point:
                node.x = right_offset + x_offset * (i - mid_point)
            else:
                node.x = 0
            node.y = level * y_offset
    min_x = min([node.x for node in nodes])
    if min_x < 0:
        offset_x_plus = -min_x
        for node in nodes:
            node.x += offset_x_plus
    return nodes


def _unique_group(devices: list[Device]) -> list[Group]:
    group_names = {
        device.server_room
        for device in devices
        if device.server_room and device.device_role == DeviceRole.access_switch
    }
    return [Group(group_name) for group_name in group_names]


def _group_by_devices(devices: list[Device]) -> list[Node]:
    nodes = [
        Node(hostname=device.hostname, device_role=device.device_role)
        for device in devices
    ]
    # for device in devices:
    #     if device.server_room and device.device_role == DeviceRole.access_switch:
    #         nodes.append(
    #             Node(
    #                 hostname=device.hostname,
    #                 device_role=device.device_role,
    #                 group=device.server_room,
    #             )
    #         )
    #     else:
    #         nodes.append(Node(hostname=device.hostname, device_role=device.device_role))
    return nodes


def topology_generator(devices: list[Device], conns: list[Connection]) -> None:
    hostname_device_mapping = {device.hostname: device for device in devices}
    d2d_conns: dict[str, dict[str, int]] = defaultdict(dict)
    # groups = _unique_group(devices)
    nodes = _group_by_devices(devices)
    nodes = _node_cord_calculator(nodes)
    links = []
    for conn in conns:
        key = conn.local_hostname + conn.remote_hostname
        if key not in d2d_conns:
            d2d_conns[key]["total"] = 1
            d2d_conns[key]["current"] = 1
        else:
            d2d_conns[key]["total"] += 1
            d2d_conns[key]["current"] += 1
    for conn in conns:
        key = conn.local_hostname + conn.remote_hostname
        total_count = d2d_conns[key]["total"]
        current_count = d2d_conns[key]["current"]
        local_device = hostname_device_mapping.get(conn.local_hostname)
        remote_device = hostname_device_mapping.get(conn.remote_hostname)
        if local_device and remote_device:
            if (
                local_device.device_role.node_level
                == remote_device.device_role.node_level
            ):
                exitX, exitY, entryX, entryY = _lr_cord_calculator(total_count)[
                    current_count
                ]
            elif (
                local_device.device_role.node_level
                > remote_device.device_role.node_level
            ):
                exitX, exitY, entryX, entryY = _dt_cord_calculator(total_count)[
                    current_count
                ]
            else:
                exitX, exitY, entryX, entryY = _td_cord_calculator(total_count)[
                    current_count
                ]
            d2d_conns[key]["current"] -= 1
            links.append(
                Link(
                    source=conn.local_hostname,
                    target=conn.remote_hostname,
                    label=f"{conn.local_interface_name}-{conn.remote_interface_name}",
                    exitX=exitX,
                    exitY=exitY,
                    entryX=entryX,
                    entryY=entryY,
                    parent_id=conn.local_hostname,
                    color=conn.if_type.interface_type_color,
                )
            )
    top = TopoGen(
        corp_name=PROJECT_CONFIG.corp_name, site_code=PROJECT_CONFIG.site_code
    )
    # top.add_groups(groups)
    top.add_nodes(nodes)
    top.add_links(links)
    top.export_xml(Path(DEFAULT_TOPOLOGY_PATH))
