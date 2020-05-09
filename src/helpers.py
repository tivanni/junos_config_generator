from logging import log_message
from system_interactions import interrupt_execution_with_errors

def validate_ip_addresses(devices):
    '''Verifies there are no duplicated address on the devices provided as input'''
    log_message(validate_ip_addresses.__name__, "validate ip addresses started")
    ip_addresses = []
    for device in devices:
        device_ips = [interface.ip_address for interface in device.interfaces_phy] + [interface.ip_address for
                                                                                      interface in device.interfaces_lo]
        ip_addresses.extend(device_ips)
    if not len(ip_addresses) == len(set(ip_addresses)):
        interrupt_execution_with_errors(validate_ip_addresses.__name__,"Duplicated Ip address found")
