Simple Juniper Config Generator

This project provides a simple juniper config generator.

At the moment, the code generates:
-device configuration:
	-hostname
	-interface configuration(both physical and logical)
-system configuration(required for the virtual lab, can be ignored if vlab is not usedb):
	-link config
	-namemap config (hostname to VM_ID mapping)

To generate the configuration, the project reads from ./config/source/ the following filesa
-devices.csv: valid devices
-physical_interfaces.csv: physical connections
-logical_interfaces.csv: logical interfaces
---config_db.xlsx can be used to facilitate the generation of the three files above. There are a certain number of functions to facilitate topology creation and link ip address assignment

The code enforces the following checks on network data validity:
-hostname:
	-alphanumerical only (doesn't allow spaces)

-interface
	-name has to match with specified regex
	-Ipv4 address has to be a valid IPv4
	-Logical interfaces are /32

-link:
	-ip addresses on two endpoints must be in same network
	-no physical loopback (interface connected to itself)

-topology:
	-no duplicated endpoint(device_interface couple)
	-all the endpoints must refer to a valid device(specified in device file)
	-no duplicate ip address

The project structure encourage abstaction:
	-constants should be specified in constants.py
	-file operations are specified in file_operations.py
	-network entities are modeled in network_entities.py
	-interaction with OS are defined in system_interactions.py
	-device config genaration is defined in config_operations
	-generic functions and feature are implemented in helpers.py
	-logging is specified in logging.py

At the beginning of each execution, all the .cfg files from previous executions are cancelled