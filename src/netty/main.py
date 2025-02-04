from netty.logger import configure_logging
from netty.project.file_parser import (
    parse_devices,
    parse_connections,
    parse_fix_ips,
    parse_project_info,
    parse_subnets,
    enrich_devices_and_connections
)
from netty.confgen.gen import config_generator
from netty.topogen.gen import topology_generator


def main() -> None:
    configure_logging()
    devices = parse_devices()
    connections = parse_connections()
    devices, connections = enrich_devices_and_connections(devices, connections)
    subnets = parse_subnets()
    fix_ips = parse_fix_ips()
    project_info = parse_project_info()

    topology_generator(devices, connections)
    config_generator(devices, connections, subnets, fix_ips, project_info)


if __name__ == "__main__":
    main()
