from system_interactions import interrupt_execution_with_errors
from constants import VALID_INTERFACE_REGEX_PHYSICAL, VALID_INTERFACE_REGEX_LOOPBACK
from ipaddress import IPv4Interface
import re

class Interface():
    '''Class defining an interface'''
    interface_regex = VALID_INTERFACE_REGEX_PHYSICAL



    def __init__(self,name,ip_address, mask,  description="None"):
        if self.is_name_valid(name):
            self.name = name.lower()
            self.description = description
            try:
                self.ip_address = IPv4Interface(f'{ip_address}{"/"}{mask}')
            except ValueError as e:
                interrupt_execution_with_errors(Interface.__init__.__name__,f"Ip Address {ip_address}/{mask} exception {e}")

    def __eq__(self,other):
        return self.name == other.name

    def __repr__(self):
        return f"{self.name}:{self.ip_address},{self.description}\n"

    def __str__(self):
        return f"{self.name}:{self.ip_address},{self.description}\n"



    def is_name_valid(self,interface_name):
        valid_interface = re.compile(self.interface_regex)
        if valid_interface.match(interface_name):
            return True
        interrupt_execution_with_errors(Interface.is_name_valid.__name__, f"Invalid Interface: {name}")

class LoopbackInterface(Interface):
    '''Class Defining a loopback interface'''

    interface_regex = VALID_INTERFACE_REGEX_LOOPBACK

    def __init__(self,name,ip_address):
        super().__init__(name,ip_address,"32",f"loopback {name}")

    def __repr__(self):
        return f"{self.name}:{self.ip_address}\n"

    def __str__(self):
        return f"{self.name}:{self.ip_address}\n"


class Device():
    '''Class rapresenting a network device
    Checks implemented:
        no spaces in hostname
        alphanumerical characters only
    '''


    def __init__(self, hostname):
        if self.is_hostname_valid(hostname):
            self.hostname = hostname.upper()
            self.interfaces_phy = []
            self.interfaces_lo = []


    def __eq__(self,other):
        return self.hostname == other.hostname

    def __str__(self):
        interfaces_phy_to_string = ''.join(sorted([str(interface) for interface in self.interfaces_phy]))
        interfaces_lo_to_string = ''.join(sorted([str(interface) for interface in self.interfaces_lo]))
        return f"{self.hostname}:\n{interfaces_phy_to_string}\n{interfaces_lo_to_string}"

    def __repr__(self):
        interfaces_phy_to_string = ''.join(sorted([str(interface) for interface in self.interfaces_phy]))
        interfaces_lo_to_string = ''.join(sorted([str(interface) for interface in self.interfaces_lo]))
        return f"{self.hostname}:\n{interfaces_phy_to_string}\n{interfaces_lo_to_string}"


    def __hash__(self):
        return hash(self.hostname)

    def is_hostname_valid(self,hostname):
        if hostname.isalnum():
            return True
        interrupt_execution_with_errors(Device.is_hostname_valid.__name__ , f"Invalid Hostname: {hostname}")

class Endpoint():
    '''Class representing a link endpont'''


    def __init__(self,device,interface):
        if isinstance(device,Device) and isinstance(interface,Interface):
            self.device = device
            self.interface = interface
            return
        interrupt_execution_with_errors(Endpoint.__init__.__name__,"Endpoint Creation: Device and/or Interface invalid")

    def __eq__(self,other):
        return self.device == other.device and self.interface == other.interface

    def __hash__(self):
        return hash(self.device.hostname + self.interface.name)

    def __repr__(self):
        return f"{self.device}{self.interface}"

class Link():
    '''Class representing a link'''


    def __init__(self, endpoint_one, endpoint_two):
        self.is_link_valid(endpoint_one,endpoint_two)
        if endpoint_one.device.hostname < endpoint_two.device.hostname:
            self.endpoint_a_end = endpoint_one
            self.endpoint_z_end = endpoint_two
        else:
            self.endpoint_a_end = endpoint_two
            self.endpoint_z_end = endpoint_one
        self.link_id = f"{self.endpoint_a_end.device.hostname}_{self.endpoint_a_end.interface.name}:{self.endpoint_z_end.interface.name}_{self.endpoint_z_end.device.hostname}"
        self.endpoint_a_end.interface.description = f"{self.endpoint_a_end.device.hostname}_{self.endpoint_a_end.interface.name}->{self.endpoint_z_end.device.hostname}_{self.endpoint_z_end.interface.name}"
        self.endpoint_z_end.interface.description = f"{self.endpoint_z_end.device.hostname}_{self.endpoint_z_end.interface.name}->{self.endpoint_a_end.device.hostname}_{self.endpoint_a_end.interface.name}"

    def is_link_valid(self,endpoint_one,endpoint_two):
        self.is_not_pysical_loopback(endpoint_one,endpoint_two)
        self.are_ip_in_same_network(endpoint_one,endpoint_two)




    def is_not_pysical_loopback(self,endpoint_one,endpoint_two):
        if endpoint_one.device.hostname == endpoint_two.device.hostname:
            interrupt_execution_with_errors(Link.is_not_pysical_loopback.__name__, "Link creation: physical loopback not supported")


    def are_ip_in_same_network(self,endpoint_one,endpoint_two):
        if not endpoint_one.interface.ip_address.network == endpoint_two.interface.ip_address.network:
            interrupt_execution_with_errors(Link.are_ip_in_same_network.__name__,
                                            "Link creation: ip addresses on link not on same network")
















