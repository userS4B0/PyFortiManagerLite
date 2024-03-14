# File: /payloads/backup.py

### IMPORTS
from src import api_handlers as api  # Importing api_handlers module from src package
from src import file_handlers as file  # Importing file_handlers module from src package

### GLOBAL VARS
# There are no global variables defined in this script.

### FUNCTIONS
def execute_backup(fgt):
    """
    Executes a backup operation for a given FortiGate device.

    Parameters:
    - fgt (dict): A dictionary containing information about the FortiGate device.

    Returns:
    - bool: True if the backup was successful, False otherwise.
    """
    # Mount the backup URL
    url = api.mount_url(fgt)
    if not url:
        return False

    # Perform the backup
    print(f'Fortigate online on {api.online_ip}, backing up...')
    try:
        bkp_data = api.req.get(url)  # Sending GET request to the mounted URL to perform backup
    except Exception as e:
        global error_message
        error_message = str(e)
        return False

    # Save and check the backup file
    file_ok = file.save_and_check_file(fgt['name'], bkp_data)  # Saving backup data to file and checking it
    return file_ok

#### ---------- EOF ---------- ####
