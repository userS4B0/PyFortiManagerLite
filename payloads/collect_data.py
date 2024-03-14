# File: /payloads/collect_data.py

### IMPORTS
import os

from src import api_handlers as api  # Importing api_handlers module from src package
from src import file_handlers as file  # Importing file_handlers module from src package
from payloads import backup # Importing backups payload

### GLOBAL VARS
# There are no global variables defined in this script.

### FUNCTIONS

def retrieve_data(fgt): # FIXME: Doesnt read the bkp file correctly
    """
    Executes an API request for a given FortiGate device.

    Parameters:
    - fgt (dict): A dictionary containing information about the FortiGate device.

    Returns:
    - bool: True if the operation was successful, False otherwise.
    """
    # Mount the backup URL
    url = api.mount_url(fgt)
    if not url:
        return False

    # Perform the backup
    print(f'Device online on {api.online_ip}, performing backup...')
    backup_file = backup.execute_backup(fgt)

    fgt_version = file.read_version_from_backup(backup_file, fgt['Name'], fgt['Managment IP 01'], fgt['Managment IP 02'])
    file.update_registry(fgt_version, os.path.join(file.DATA_DIR, 'registry.csv'))