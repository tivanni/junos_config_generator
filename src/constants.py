#source constants
SOURCE_BASEPATH = '../config/source/'
FILE_DEVICES = SOURCE_BASEPATH + 'devices.csv'
FILE_PHY_INTERFACES = SOURCE_BASEPATH + 'physical_interfaces.csv'
FILE_LO_INTERFACES = SOURCE_BASEPATH + 'logical_interfaces.csv'
#logs constants
LOGS_BASEPATH = '../logs/'
FILE_LOGS = LOGS_BASEPATH + 'logs.txt'
#output_constants
OUTPUT_BASEPATH = '../config/output/'
OUTPUT_DEVICE_CONFIG = OUTPUT_BASEPATH + 'device_config/'
OUTPUT_SYSTEM_CONFIG = OUTPUT_BASEPATH + 'system_config/'
OUTPUT_LINKS_CFG = 'links'
OUTPUT_NAMEMAP = 'namemap'
#validation_constants
VALID_INTERFACE_REGEX_PHYSICAL = '^(xe-0/0/(1[0-9]|[0-9]))$'
VALID_INTERFACE_REGEX_LOOPBACK = '^(lo[0-9]+)$'
#config_constants
CONFIG_INITIALIZE = 'configure exclusive'
CONFIG_FINALIZE = 'commit and-quit'
#VM ID constant
VM_ID_START = 2700