import logging

from netty.logger import configure_logging
from netty.project.file_parser import (
    parse_network_data,
    parse_project_info,
    enrich_devices_and_connections,
)
from netty.genconf.gen import config_generator
from netty.gentopo.topogen import topology_generator

logger = logging.getLogger(__name__)


def gen() -> None:
    configure_logging()
    devices, connections, subnets, fix_ips = parse_network_data()
    if len(devices) == 0:
        logging.warning("parse network data: no devices founded")
    devices, connections = enrich_devices_and_connections(devices, connections)
    project_info = parse_project_info()
    if len(connections) > 0:
        topology_generator(devices, connections)
    config_generator(devices, connections, subnets, fix_ips, project_info)
