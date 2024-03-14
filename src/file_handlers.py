# File: /src/file_handlers.py

### IMPORTS
import sys
import os
import csv
from datetime import datetime

### GLOBAL VARS
DATE = datetime.now().strftime('%m-%d-%Y')      # Today's date in the format mm-dd-yyyy
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))   # Path to the directory where this script is located
APP_DIR = os.path.dirname(CURRENT_DIR) # Global Path of the App
DATA_DIR = os.path.join(APP_DIR, 'data')     # Path to the backups folder
BKP_FOLDER = os.path.join(DATA_DIR, 'backups', DATE)     # Path to the backups folder
LOGS_FOLDER = os.path.join(DATA_DIR, 'logs')     # Path to the logs folder

error_message = '',''

### FUNCTIONS
def create_folders():

    try:
        # Create the backups and logs folders if they don't exist
        # exist_ok=True prevents the function from raising an exception if the folder already exists
        os.makedirs(BKP_FOLDER, exist_ok=True)
        os.makedirs(LOGS_FOLDER, exist_ok=True)
    except Exception as e:
        print(f'Error creating folders: {e}')
        input('Press ENTER to exit...')
        sys.exit()

def read_inventory():

    try:
        # Read the fortigates.csv file and convert it to a list of dictionaries
        with open(os.path.join(DATA_DIR, 'inventory.csv'), 'r') as file:
            fortigates = list(csv.DictReader(file, delimiter=','))
    except FileNotFoundError as e:
        print(f'Inventory file not found: {e}')
        input('Press ENTER to exit...')
        sys.exit()
    except Exception as e:
        print(f'Error reading inventory file: {e}')
        input('Press ENTER to exit...')
        sys.exit()

    return fortigates

def save_and_check_file(name, data):

    # Access the global variable error_message
    global error_message

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
        error_message = 'Invalid backup file'
        return True
    
    except Exception as e:
        error_message = str(e)
        return False
#### ---------- EOF ---------- ####