from netty.topogen.gen import TopoGen
from netty.topogen.diagram import Link, Node
from netty.arch import DeviceRole
from pathlib import Path

nodes = [
    Node(hostname="csw1", device_role=DeviceRole.core_switch),
    Node(hostname="csw2", device_role=DeviceRole.core_switch),
    Node(hostname="wac1", device_role=DeviceRole.wlan_ac),
    Node(hostname="wac2", device_role=DeviceRole.wlan_ac),
    Node(hostname="asw1", device_role=DeviceRole.access_switch)
]

links = [
    Link(source="csw1", target="csw2",label="g0/45-g0/46", parent_id="csw1"),
    Link(source="csw1", target="csw2",label="g0/46-g0/45", parent_id="csw1"),
    Link(source="csw1", target="csw2",label="g0/44-g0/44", parent_id="csw1"),
    Link(source="csw1", target="wac1",label="g0/1-g0/43", parent_id="csw1"),
    Link(source="csw1", target="wac1",label="g0/2-g0/42", parent_id="csw1"),
    Link(source="csw2", target="wac2",label="g0/1-g0/43", parent_id="csw2"),
    Link(source="csw2", target="wac2",label="g0/2-g0/42", parent_id="csw2"),
    Link(source="csw1", target="asw1", label="g0/48-g0/41", parent_id="csw1"),
    Link(source="csw2", target="asw1", label="g0/48-g0/41", parent_id="csw2")
]

top = TopoGen(
    corp_name="test",
    site_code="CNPEK01"
)
for node in nodes:
    top.add_node(node)
for link in links:
    top.add_link(link)
top.export_xml(Path("./test.drawio"))