# Netty Network Automation Tool
## Introduction
This project aims to automate the generation of network device configurations and network topology diagrams using Draw.io XML files based on network device tables, interconnection tables, and subnet planning tables. It provides a streamlined and efficient way to manage and visualize network configurations and topologies. 

It's only aims to provide support for highly standard network architecture, such as traditional L3 network, `core_switch/access_switch`, `core_switch/distribution_switch/access_switch` and uplink to firewall/router/internet_switch for multiple ISP providers.

This project is still under development, here are the few things planning to do:
1. improve multi-vendor support, enrich devicetypes libs and jinja2 template for highly optimize configuration, support vrrp model(current only support stackwise)
2. improve topology layout algorithm， make it's more beautiful and easy to adjust
3. add support for ZTP (zero-touch-provisioning) for configuration push in day-one network construction



## Architecture Overview
The software architecture is divided into the following layers:

### **Network Architecture Layer**
This layer defines the data models for network device vendors, platforms, device roles, and device models. It serves as the foundation of the system. The vendor and platform determine which corresponding factory is used to generate configurations in the upper layers. The device role and model influence the device's hierarchy in the network and some differentiated content in configuration generation.
#### DeviceRole
> device_role is a key concept of network device, define the role and function of hardware device in network layers.
- Core Switch
- Distribution Switch
- Access Switch
- Firewall
- Internet Switch
- WLAN AC
- WLAN AP
- SDWAN Hub

> platform: basically, use `netmiko platform` for hardware, it defined under `collections/devicetypes` directory
- cisco_iosxe
- ruijie
- huawei_vrp
> device_type: define device metadata of hardware

### **Project Parsing Layer**
This layer is responsible for defining models for devices, interconnection tables, and subnet planning. It parses CSV files and maps the data onto these models.

### **Configuration Generation Layer**
Based on different vendors and platforms, this layer implements various factories. It uses a dispatcher model to distribute configuration generation tasks to the appropriate factories.
Each manufacturer will define different factory for different product family, it will render a object to jinja2 template for configuration generation, so it can be customized as every corp requirements.
See file structure:
```
├── __init__.py
├── dispatcher.py        # dispatcher factory class for different devices
├── factory              # basic factory for different product family
│   ├── __init__.py
│   ├── firewall_factory.py
│   ├── switch_factory.py
│   └── wlc_factory.py
├── gen.py              # configuration gen
├── manufacturer        # various vendor implementation for config gen
│   ├── cisco
│   ├── fortinet
│   │   ├── __init__.py
│   │   ├── docs
│   │   ├── firewall.py
│   │   ├── firewall_enhance_ha.j2
│   │   ├── firewall_ha_intsw.j2
│   │   ├── firewall_single.j2
│   │   ├── sdwan_hub.j2
│   │   └── sdwan_spoke.j2
│   ├── huawei
│   │   ├── __init__.py
│   │   ├── switch.j2
│   │   └── switch.py
│   └── ruijie
│       ├── __init__.py
│       ├── switch.j2
│       └── switch.py
└── utils.py
```

###  **Topology Generation Layer**
Using the interconnection table and device table models, this layer automatically generates Draw.io XML files for optimized network topology diagrams.

## Key Features
- **Automated Configuration Generation**: Generates network device configurations based on predefined templates and input data.
- **Draw.io Topology Generation**: Automatically creates network topology diagrams in Draw.io format.
- **CSV File Parsing**: Easily imports and parses CSV files containing network device, interconnection, and subnet planning data.
- **Flexible and Extensible**: Supports multiple vendors, platforms, device roles, and models, making it adaptable to various network environments.
## Getting Started
### Prerequisites
- Python environment set up (recommended version: Python 3.12)
- Required Python libraries (install using pip install -r requirements-dev.txt)
- Draw.io Desktop or Draw.io online account for viewing and editing generated topology diagrams
### Installation
Clone the repository:
```bash
git clone https://github.com/your-username/network-automation-tool.git
cd network-automation-tool
# Install the required Python libraries:
pip install -r requirements.txt
```
## Usage
1. Prepare project info and CSV files:
> example: create a new project under project directory with corp_name: ACME and site_code: ACME-PEK01, country_code: US
> after command line executing, it will generate some files under the directory.
```bash
cd src/netty/cli
python cli.py new {{corp_name}} {{site_code}} {{country_code}}
```
- **`config.yaml`**: defined the baseline of network configuration, which include `baseline_config`, `system_config`, `snmp_config` and `netflow_config`, `aaa_config`,customize as be made for single project.
- `devices.csv`: defines hardware list with built-in formatted
- `connections.csv`: defines the inter-connections between network devices
- `fix_ips`: dhcp pool fixed ip addresses, used for dhcp config generation
- `subnets`: dhcp pool and switch SVI generation

1. Run the Script:
Execute the main script to generate configurations and topology diagrams:
```bash
python main.py
```
1. Check Outputs:
Configurations and Draw.io XML files topology will be saved in the `project/{{corp_name}}/{{site_code}}` directory.

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please feel free to open an issue or submit a pull request.

## License
This project Licensed under the Apache License, Version 2.0
