import sys
import os
import csv
import logging
from datetime import datetime

# Global variables
DATE = datetime.now().strftime('%Y-%m-%d')
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(APP_DIR, 'data')
BKP_FOLDER = os.path.join(DATA_DIR, 'backups', DATE)
LOGS_FOLDER = os.path.join(DATA_DIR, 'logs')
error_message = ''

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s] %(message)s',
    filename=os.path.join(LOGS_FOLDER, f'pfgtmgrl_{DATE}.log'),
    filemode='a'
)
logger = logging.getLogger('PyFortiManagerLite')

def create_folders():
    """
    Creates the necessary folders for backups and logs.
    """
    try:
        logger.info('Attempting to create Backup and Logs folder')
        os.makedirs(BKP_FOLDER, exist_ok=True)
        os.makedirs(LOGS_FOLDER, exist_ok=True)
        logger.info('Backup and Logs folders created')
    except Exception as e:
        logger.exception(f'Error creating folders: {e}')
        print(f'Error creating folders: {e}')
        input('Press ENTER to exit...')
        logger.warning('Exiting program')
        sys.exit()

def read_inventory():
    """
    Reads the inventory data from the 'inventory.csv' file.

    Returns:
        list: A list of dictionaries containing information about the FortiGate devices.
    """
    try:
        logger.info('Attempting to read inventory.csv file')
        with open(os.path.join(DATA_DIR, 'inventory.csv'), 'r') as file:
            fortigates = list(csv.DictReader(file, delimiter=','))
        logger.info('inventory.csv read, fortigates loaded')
        return fortigates
    except FileNotFoundError as e:
        logger.exception(f'Inventory file not found: {e}')
    except Exception as e:
        logger.exception(f'Error reading inventory file: {e}')
    print(f'Error reading inventory file: {e}')
    input('Press ENTER to exit...')
    logger.warning('Exiting program')
    sys.exit()

def save_and_check_file(name, data):
    """
    Saves the backup data to a file and checks if it is a valid FortiGate configuration file.

    Parameters:
        name (str): The name of the FortiGate device.
        data (bytes): The backup data to be saved.

    Returns:
        bool: True if the backup file is saved and valid, False otherwise.
    """
    global error_message
    file_path = os.path.join(BKP_FOLDER, f'{name}-bkp-{DATE}.conf')
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        with open(file_path, 'r') as file:
            first_line = file.readline()
            if first_line.startswith('#config-version'):
                return True
        os.remove(file_path)
        logger.error('Invalid backup file')
        error_message = 'Invalid backup file'
        return False
    except Exception as e:
        logger.error(str(e))
        error_message = str(e)
        return False
