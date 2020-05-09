import sys
from logging import *
from os import remove as remove_file
import glob

def interrupt_execution_with_errors(func_name, message):
    '''Interrupt the execution with errors, printing and logging a message'''
    print(f'CRITICAL: {message.upper()}')
    log_message(func_name, message)
    sys.exit('ERRORS')

def initilize_enviroment():
    '''Deletes all files matched by regex in OUTPUT directory'''
    log_message(initilize_enviroment.__name__, 'initializing enviroment started')
    file_device_config_regex = "{}*.cfg".format(OUTPUT_DEVICE_CONFIG)
    files_device_config = glob.glob(file_device_config_regex, recursive=False)
    file_system_config_regex = "{}*.cfg".format(OUTPUT_SYSTEM_CONFIG)
    files_system_config = glob.glob(file_system_config_regex, recursive=False)
    files = files_device_config + files_system_config
    for file in files:
        try:
            remove_file(file)
        except OSError as e:
            interrupt_execution_with_errors(initilize_enviroment.__name__,f"file {file} exception {e.strerror}")
    log_message(initilize_enviroment.__name__, 'initializing enviroment complete')