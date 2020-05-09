from logging import log_message
from system_interactions import interrupt_execution_with_errors
from constants import *
from network_entities import Device, Interface, LoopbackInterface, Endpoint, Link


def read_devices():
    '''Read Devices from FILE_DEVICES and return a list with hostnames
    Checks implemented:
        no duplicates
    '''
    log_message(read_devices.__name__,'device reading started')
    devices = []
    devices_read = read_lines_from_file(FILE_DEVICES)
    #check for duplicates
    if not len(devices_read) == len(set(devices_read)):
        interrupt_execution_with_errors(read_devices.__name__,'duplicated hostnames found')
    for hostname in devices_read:
        device = Device(hostname)
        devices.append(device)
    log_message(read_devices.__name__, 'device reading completed')
    return devices


def read_topology(devices_valid):
    '''Read from FILE_PHY_INTERFACES, updates Device info and return topology
    Check implemented:
        no duplicated endpoint
        no physical loopback (cable connected to same device)
        endpoint using valid device
     '''
    log_message(read_topology.__name__, 'physical interfaces reading started')
    lines = read_lines_from_file(FILE_PHY_INTERFACES)
    devices = []
    endpoints = []
    links = []
    devices_valid_dict = { device.hostname: device for device in devices_valid}

    for line in lines:
        if ':' in line: #link_id is constructed using ':'
            fields = line.split(',')
            link_id = fields[0]
            network_base_input = fields[1]
            network_prefix_input = fields[2]
            a_and_device_input = fields[3]
            a_end_interface_input = fields[4]
            a_end_host_ip_input = fields[5]
            z_and_device_input = fields[6]
            z_end_interface_input = fields[7]
            z_end_host_ip_input = fields[8]
            a_end_device = Device(a_and_device_input)
            a_and_interface = Interface(a_end_interface_input,f'{network_base_input}.{a_end_host_ip_input}', network_prefix_input)
            z_end_device = Device(z_and_device_input)
            z_and_interface = Interface(z_end_interface_input, f'{network_base_input}.{z_end_host_ip_input}', network_prefix_input)
            a_end_endpoint = Endpoint(a_end_device,a_and_interface)
            z_end_endpoint = Endpoint(z_end_device,z_and_interface)
            devices.append(a_end_device)
            devices.append(z_end_device)
            endpoints.append(a_end_endpoint)
            endpoints.append(z_end_endpoint)
            link = Link(a_end_endpoint,z_end_endpoint)
            try:
                devices_valid_dict[link.endpoint_a_end.device.hostname].interfaces_phy.append(link.endpoint_a_end.interface)
                devices_valid_dict[link.endpoint_z_end.device.hostname].interfaces_phy.append(link.endpoint_z_end.interface)
            except KeyError:
                print(f"{a_end_device.hostname} and/or {z_end_device.hostname} not found in in devices_valid")
            links.append(link)

    if not set(devices).issubset(set(devices_valid)):
        print(f"Invalid devices found:{set(devices) - set(devices_valid)}")

        interrupt_execution_with_errors(read_topology.__name__,"Invalid device read")

    if not len(endpoints) == len(set(endpoints)):
        interrupt_execution_with_errors(read_topology.__name__, "Physical Duplicated endpoint found")

    log_message(read_topology.__name__, 'physical interfaces reading finished')

    return links




def read_lines_from_file(filename):
    '''Given a filename, returns a list with all the non-empty and uncommented lines, stripped'''
    log_message(read_lines_from_file.__name__,'file reading started')
    file_handler = open(filename, errors='ignore', encoding='utf-8-sig')
    lines = []
    for line in file_handler:
        line = line.strip()
        if line and not line.startswith('#'):
            lines.append(line)
    file_handler.close()
    log_message(read_lines_from_file.__name__, 'file reading completed')
    if not lines: #check for empty file
        interrupt_execution_with_errors(read_lines_from_file.__name__, f'{filename} is empty')
    return lines

def write_lines_to_file(filename,lines):
    '''Given a filename and a list, writes each list element as a line in the file'''
    log_message(write_lines_to_file.__name__, 'lines writing started')
    file_handler = open(filename,'a+')
    lines = map(lambda x:x+'\n', lines)
    file_handler.writelines(lines)
    file_handler.close()
    log_message(write_lines_to_file.__name__, 'lines writing completed')

def write_device_config_to_file(device, config):
    log_message(write_lines_to_file.__name__, 'write device config started')
    filename = "{}{}.cfg".format(OUTPUT_DEVICE_CONFIG,device)
    write_lines_to_file(filename,config)
    log_message(write_lines_to_file.__name__, 'write device config completed')


def write_system_config_to_file(system_config_file, config):
    log_message(write_lines_to_file.__name__, 'write system config started')
    filename = "{}{}.cfg".format(OUTPUT_SYSTEM_CONFIG,system_config_file)
    write_lines_to_file(filename,config)
    log_message(write_lines_to_file.__name__, 'write system config completed')


def read_loopback(devices_valid):
    '''Ready from FILE_LO_INTERFACES, updates Device. No return value
    Check implemented:
        no duplicated endpoint
        endpoint using valid device
    '''
    log_message(read_loopback.__name__, 'looback interfaces reading started')
    lines = read_lines_from_file(FILE_LO_INTERFACES)
    devices = []
    endpoints = []
    devices_valid_dict = { device.hostname: device for device in devices_valid}

    for line in lines:
        fields = line.split(',')
        device = Device(fields[0])
        devices.append(device)
        loopback_interface = LoopbackInterface(fields[1],fields[2])
        endpoint = Endpoint(device,loopback_interface)
        endpoints.append(endpoint)
        try:
            devices_valid_dict[device.hostname].interfaces_lo.append(loopback_interface)
        except KeyError:
            print(f"{device.hostname} key not found in devices_valid")

    if not set(devices).issubset(set(devices_valid)):
        print(f"Invalid devices found:{set(devices) - set(devices_valid)}")
        interrupt_execution_with_errors(read_loopback.__name__,"Invalid device read")

    if not len(endpoints) == len(set(endpoints)):
        interrupt_execution_with_errors(read_loopback.__name__, "Loopback Duplicated endpoint found")

    log_message(read_loopback.__name__, 'loopback interfaces reading finished')













