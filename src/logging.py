from constants import *
import time

def log_initialize():
    '''create/reset log file'''
    file_handler = open(FILE_LOGS, 'w')
    file_handler.close()


def log_message(func_name , message):
    '''Log Message in FILE_LOGS'''
    if message:
        localtime = time.asctime(time.localtime(time.time()))
        file_handler = open(FILE_LOGS,'a')
        file_handler.write(f"{localtime} {func_name}: {message} \n")
        file_handler.close()