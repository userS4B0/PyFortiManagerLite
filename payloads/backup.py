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
    file.logger.info(f'Attempting to create Backup at [{fgt["Name"]}]')
    
    # Mount the backup URL
    file.logger.info(f'Attempting to mount URL')
    url = api.mount_url(fgt)
    if not url:
        file.logger.error(f'No URL was Provided')
        return False

    # Perform the backup
    file.logger.info(f'URL Mounted, performing backup at [{api.online_ip}]')
    print(f'Fortigate online on {api.online_ip}, backing up...')
    try:
        file.logger.info(f'Attempting API request to {url}')
        bkp_data = api.req.get(url)  # Sending GET request to the mounted URL to perform backup
    except Exception as e:
        file.logger.exception(f'An Exception Ocurred: {str(e)}')
        return False

    # Save and check the backup file
    file.logger.info(f'Checking Backup File [{fgt['Name']}]')
    file_ok = file.save_and_check_file(fgt['Name'], bkp_data)  # Saving backup data to file and checking it
    file.logger.info(f'Backup File [{fgt['Name']}] is correct!')
    return file_ok

#### ---------- EOF ---------- ####