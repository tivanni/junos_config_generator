from logging import log_message
from file_operations import write_device_config_to_file, write_system_config_to_file
from constants import *

def initialize_config_files(devices):
    '''Initialize the config file for each device'''
    log_message(initialize_config_files.__name__, 'initializing config started')
    config = []
    config.append(CONFIG_INITIALIZE)
    for device in devices:
        write_device_config_to_file(device.hostname,config)
    log_message(initialize_config_files.__name__, 'initializing config completed')

def generate_hostname_config(devices):
    '''Generates the configuration required to set the hostname
    Hostname is set to device name'''
    log_message(generate_hostname_config.__name__, 'initializing hostname config started')
    for device in devices:
        config_lines = [f'set system host-name {device.hostname}']
        write_device_config_to_file(device.hostname,config_lines)
    log_message(generate_hostname_config.__name__, 'initializing hostname config finished')


def finilize_config_files(devices):
    '''Finilize the config file for each device'''
    log_message(finilize_config_files.__name__, 'finalizing config started')
    config = []
    config.append(CONFIG_FINALIZE)
    for device in devices:
        write_device_config_to_file(device.hostname, config)
    log_message(finilize_config_files.__name__, 'finalizing config completed')


def generate_ip_address_config(devices):
    '''Generates interface configuration for each file'''
    log_message(generate_ip_address_config.__name__,"generate ip address config started")
    for device in devices:
        interfaces = device.interfaces_phy + device.interfaces_lo
        ip_config_lines = [f"set interfaces {interface.name} unit 0 family inet address {interface.ip_address.with_prefixlen}" for interface in interfaces]
        desc_config_lines = [f"set interfaces {interface.name} description {interface.description}" for interface in interfaces]
        config_lines = ip_config_lines + desc_config_lines
        write_device_config_to_file(device.hostname,config_lines)
    log_message(generate_ip_address_config.__name__,"generate ip address config finished")


def generate_links_config(links):
    '''Generate link.cfg with the following format:
    DeviceA interfaceA DeviceB interfaceB
    '''
    log_message(generate_links_config.__name__,"generate links config started")
    links_config = [f"{link.endpoint_a_end.device.hostname} {link.endpoint_a_end.interface.name} {link.endpoint_z_end.device.hostname} {link.endpoint_z_end.interface.name}" for link in links]
    write_system_config_to_file(OUTPUT_LINKS_CFG,links_config)
    log_message(generate_links_config.__name__,"generate links config finished")


def generate_namemap_config(devices):
    '''Generate namemap with the following format:
    VMID DEVICE_HOSTNAME
    VMID starts  from VM_ID_START set in constants and then incremented by one unit
    '''
    log_message(generate_namemap_config.__name__,"generate namemap config started")
    config = []
    id = VM_ID_START
    devices_sorted = sorted(devices, key = lambda e:e.hostname)
    for device in devices_sorted:
        config.append(f"{id} {device.hostname}")
        id = id + 1
    write_system_config_to_file(OUTPUT_NAMEMAP,config)
    log_message(generate_namemap_config.__name__,"generate namemap config finished")