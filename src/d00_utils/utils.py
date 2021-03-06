import os
import logging

def flush_file(file_name):
    if (os.path.isfile(f'data/raw/{file_name}')):
        os.remove(f'data/raw/{file_name}')
        logging.info(f'{file_name} found, deleting...')