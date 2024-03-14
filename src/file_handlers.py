# File: /src/file_handlers.py

### IMPORTS
import sys
import os
import csv
import logging

from datetime import datetime

# from src.log_handlers import logger

### GLOBAL VARS
DATE = datetime.now().strftime('%Y-%m-%d')  # Today's date in the format yyyy-mm-dd
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))  # Path to the directory where this script is located
APP_DIR = os.path.dirname(CURRENT_DIR)  # Global Path of the App
DATA_DIR = os.path.join(APP_DIR, 'data')  # Path to the data directory
BKP_FOLDER = os.path.join(DATA_DIR, 'backups', DATE)  # Path to the backups folder
LOGS_FOLDER = os.path.join(DATA_DIR, 'logs')  # Path to the logs folder

error_message = ''  # Variable to store error messages


### LOGGER OBJECT

logging.basicConfig( # Configure the logging system
    level=logging.INFO,  # Minimum logging level (INFO in this case)
    format='[%(asctime)s][%(levelname)s] %(message)s',  # Log message format
    filename=os.path.join(LOGS_FOLDER, f'pfgtmgrl_{DATE}.log'),  # Log file path
    filemode='a'  # Log file mode (append)
)

# Create a Logger object

logger = logging.getLogger('PyFortiManagerLite') # TODO: Handle FileNotFoundExcepion when importing if logs folder is not created

### FUNCTIONS
def create_folders():
    """
    Creates the necessary folders for backups and logs.

    Returns:
    - logger object
    """
    
    try:
        # Create the backups and logs folders if they don't exist
        # exist_ok=True prevents the function from raising an exception if the folder already exists
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
    - list: A list of dictionaries containing information about the FortiGate devices.
    """
    try:
        # Read the fortigates.csv file and convert it to a list of dictionaries
        logger.info('Attempting to read inventory.csv file')
        with open(os.path.join(DATA_DIR, 'inventory.csv'), 'r') as file:
            fortigates = list(csv.DictReader(file, delimiter=','))
        logger.info('inventory.csv readed, fortigates loaded')

    except FileNotFoundError as e:
        logger.exception(f'Inventory file not found: {e}')
        print(f'Inventory file not found: {e}')
        input('Press ENTER to exit...')

        logger.warning('Exiting program')
        sys.exit()

    except Exception as e:
        logger.exception(f'Error reading inventory file: {e}')
        print(f'Error reading inventory file: {e}')
        input('Press ENTER to exit...')
        
        logger.warning('Exiting program')
        sys.exit()

    return fortigates

# # FIXME: Doesnt read the bkp file correctly
# def read_registry():
#     """
#     Reads the inventory data from the 'registry.csv' file.

#     Returns:
#     - list: A list of dictionaries containing information about the FortiGate devices.
#     """
#     try:
#         # Read the fortigates.csv file and convert it to a list of dictionaries
#         logger.info('Attempting to read registry.csv file')
#         with open(os.path.join(DATA_DIR, 'registry.csv'), 'r') as file:
#             fortigates = list(csv.DictReader(file, delimiter=','))
#         logger.info('inventory.csv readed')
#     except FileNotFoundError as e:
#         logger.exception(f'Registry file not found: {e}')
#         print(f'Registry file not found: {e}')
#         input('Press ENTER to exit...')
#         sys.exit()
#     except Exception as e:
#         logger.exception(f'Error reading registry file: {e}')
#         print(f'Error reading registry file: {e}')
#         input('Press ENTER to exit...')
#         logger.warning('Exiting program')
#         sys.exit()

#     return fortigates

def save_and_check_file(name, data):
    """
    Saves the backup data to a file and checks if it is a valid FortiGate configuration file.

    Parameters:
    - name (str): The name of the FortiGate device.
    - data (bytes): The backup data to be saved.

    Returns:
    - bool: True if the backup file is saved and valid, False otherwise.
    """
    global error_message  # Access the global variable error_message

    # Path to the backup file
    file_path = os.path.join(BKP_FOLDER, f'{name}-bkp-{DATE}.conf')
    
    try:
        # Save the backup data to a file
        with open(file_path, 'wb') as file:
            for line in data:
                file.write(line)

        # Check if the file is a valid Fortigate configuration file
        with open(file_path, 'r') as file:
            first_line = file.readline()
            if first_line.startswith('#config-version'):
                return True
        
        # If the file is not valid, delete it and change the error_message variable
        os.remove(file_path)
        logger.error('Invalid backup file')
        error_message = 'Invalid backup file'
        return False
    
    except Exception as e:
        logger.error(str(e))
        error_message = str(e)
        return False

# # FIXME: Doesnt read the bkp file correctly
# def read_version_from_backup(backup_file, name, mgmt_ip1, mgmt_ip2):
#     # Get the first line of the file
#     try:
#         with open(backup_file, 'r') as f:
#             version = f.readline().strip()
#             # check if it contains a string similar to #config-version=FWF30E-6.2.15-FW-build1378-230605:opmode=0:vdom=0:user=test
#             if version.startswith('#config-version='):
#                 # Get after the first '=' until the first ':'
#                 version = version.split('=')[1].split(':')[0]
#                 # Split the version string by '-' and get a list
#                 version = version.split('-')
#                 version.pop(2)
#                 version.pop(3)
#                 #Add the name of the firewall to the list of versions
#                 version.insert(0, name)
#                 version.insert(1, mgmt_ip1)
#                 version.insert(2, mgmt_ip2) 
#                 #Return the list of versions
#                 return version
#     except Exception as e:
#         logger.exception(f'Unexpected error: {e}')
#         print(f'Unexpected error: {e}')

# # FIXME: Doesnt read the bkp file correctly
# def update_registry(data, filename):

#     # if not os.path.isfile(filename):
#     #     with open(filename, 'w') as f:
#     #         f.write('Name,Management IP 01,Management IP 02,Model,Version,Build\n')
#     #         #For each firewall in the list of versions write the name, model, version and build
#     #         f.write(','.join(data) + '\n')
#     # else:
#     #     #If the file exists, open it in append mode and write the name, model, version and build
#     #     with open(filename, 'a') as f:
#     #         f.write(','.join(data) + '\n')

#     if not os.path.isfile(filename):
#         with open(filename, 'w') as f:
#             f.write('Name,Management IP 01,Management IP 02,Model,Version,Build\n')
#             f.close
#         print("File registry Created")
#     else:
#         print("File registry existent\n output to join")
#         print(f'{data}')

#### ---------- EOF ---------- ####
