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

from dataclasses import dataclass
import xml.etree.ElementTree as ET
from uuid import uuid4

from netty.arch import DeviceRole
from netty.utils.random_factory import generate_random_mx_point


@dataclass
class Group:
    group_name: str

    def to_xml(self) -> ET.Element:
        return ET.Element(
            "mxCell",
            id=self.group_name,
            style="group",
            value="",
            vertex="1",
            connectable="0",
            parent="0",
        )


@dataclass
class Node:
    hostname: str
    device_role: DeviceRole
    width: int = 80
    height: int = 80
    group: str | None = None  # not use now
    x: int = 0
    y: int = 0

    def to_xml(self) -> ET.Element:
        style = self.device_role.drawio_style
        if self.group is not None:
            parent = self.group
        else:
            parent = "1"
        mxCell = ET.Element(
            "mxCell",
            id=self.hostname,
            value=self.hostname,
            style=(
                "verticalLabelPosition=bottom;"
                "html=1;"
                "verticalAlign=top;"
                "aspect=fixed;align=center;"
                "pointerEvents=1;"
                f"{style['style']}"
                ""
            ),
            vertex="1",
            parent=parent,
        )
        mxGeometry = ET.SubElement(
            mxCell, "mxGeometry", width=style["width"], height=style["height"]
        )
        if self.x != 0:
            mxGeometry.set("x", str(self.x))
        if self.y != 0:
            mxGeometry.set("y", str(self.y))
        mxGeometry.set("as", "geometry")
        return mxCell


@dataclass
class Link:
    source: str
    target: str
    label: str
    parent_id: str
    color: str = "#007FFF"
    direction: str | None = None
    entryX: float = 0
    entryY: float = 0
    exitX: float = 0
    exitY: float = 0

    def __post_init__(self):
        self.link_id = str(uuid4())

    def to_link_xml(self) -> ET.Element:
        if self.entryX != 0 or self.entryY != 0 or self.exitX != 0 or self.exitY != 0:
            style = (
                "edgeStyle=none;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontSize=6;"
                f"entryX={self.entryX};entryY={self.entryY};entryDx=0;entryDy=0;"
                f"exitX={self.exitX};exitY={self.exitY};exitDx=0;exitDy=0;"
                f"endFill=0;endArrow=none;strokeColor={self.color}"
            )
        else:
            style = (
                "edgeStyle=none;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
                f"endFill=0;endArrow=none;strokeColor={self.color}"
            )

        mxCell = ET.Element(
            "mxCell",
            id=self.link_id,
            style=style,
            source=self.source,
            target=self.target,
            edge="1",
            parent="1",
        )
        mxGeometry = ET.SubElement(
            mxCell,
            "mxGeometry",
        )
        mxGeometry.set("relative", "1")
        mxGeometry.set("as", "geometry")
        return mxCell

    def to_link_label_xml(self) -> ET.Element:
        style = (
            "edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=6;"
        )
        mxCell = ET.Element(
            "mxCell",
            id=str(uuid4()),
            value=self.label,
            style=style,
            parent=self.link_id,
            vertex="1",
            connectable="0",
        )
        mxGeometry = ET.SubElement(mxCell, "mxGeometry")
        mxGeometry.set("x", str(generate_random_mx_point()))
        mxGeometry.set("relative", "1")
        mxGeometry.set("as", "geometry")
        mxPoint = ET.SubElement(mxGeometry, "mxPoint")
        mxPoint.set("as", "offset")
        return mxCell

@dataclass
class RackUnit:
    rack_name: str
    hostname: str
    u_position: int
    u_height: int

    def to_xml(self) -> ET.Element:
        mxCell = ET.Element(
            "mxCell",
            id=self.hostname,
            value=self.hostname,
            style="shape=mxgraph.aws3.rack;whiteSpace=wrap;html=1;align=center;verticalAlign=top;spacingTop=0;spacingLeft=0;spacingRight=0;fillColor=#ffffff;strokeColor=#000000;strokeWidth=1;size=80;points=[];collapsible=0;connectable=0;container=1;recursiveResize=0;",
            vertex="1",
            parent=self.rack_name,
        )
        mxGeometry = ET.SubElement(
            mxCell, "mxGeometry", width="80", height="80",
        )
        mxGeometry.set("as", "geometry")
        mxGeometry.set("x", "0")
        mxGeometry.set("y", str(self.u_position * 80))
        return mxCell