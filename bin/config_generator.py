from file_operations import read_devices, read_topology , read_loopback
from config_operations import initialize_config_files, generate_hostname_config, finilize_config_files, \
    generate_ip_address_config, generate_links_config,generate_namemap_config
from system_interactions import initilize_enviroment
from network_entities import Device,Interface,Endpoint, LoopbackInterface
from helpers import validate_ip_addresses


def main():
    initilize_enviroment()
    devices = read_devices()
    links = read_topology(devices)
    read_loopback(devices)
    validate_ip_addresses(devices)
    initialize_config_files(devices)
    generate_hostname_config(devices)
    generate_ip_address_config(devices)
    finilize_config_files(devices)
    generate_links_config(links)
    generate_namemap_config(devices)

    for device in devices:
        print(device)

















if __name__ == "__main__":
    main()