# File: /payloads/backup.py

### IMPORTS
from src import api_handlers as api
from src import file_handlers as file

### GLOBAL VARS


### FUNCTIONS
def execute_backup(fgt):

    # Mount the backup URL
    url = api.mount_url(fgt)
    if not url: return False

    # Perform the backup
    print(f'Fortigate online on {api.online_ip}, backing up...')
    try:
        bkp_data = api.req.get(url)
    except Exception as e:
        global error_message
        error_message = str(e)
        return False

    # Save and check the backup file
    file_ok = file.save_and_check_file(fgt['name'], bkp_data)
    return file_ok

#### ---------- EOF ---------- ####