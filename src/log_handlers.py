# File: /src/log_handlers.py

### IMPORTS
import os
import sys
from datetime import datetime
from src import file_handlers as file  # Importing file_handlers module from src package

### GLOBAL VARS
DATE = datetime.now().strftime('%Y-%m-%d')  # Today's date in the format yyyy-mm-dd
TIME = datetime.now().strftime('%H:%M:%S')  # Today's time in the format h:m:s

### FUNCTIONS
def create_log():
    """
    Creates a log file for backup operations.

    Returns:
    - file object: The opened log file in append mode.
    """
    try:
        # Create log file and keep it open for writing
        return open(os.path.join(file.LOGS_FOLDER, f'pfgtmgrl_{DATE}.log'), 'a')
    except Exception as e:
        print(f'Error creating the log file: {e}')
        input('Press ENTER to exit...')
        sys.exit()

def log(msg):
    return f'[{DATE}][{TIME}] pyfgtmgrl: {msg}\n'

def log_error(msg):
    return log(f'ERROR: {msg}')

#### ---------- EOF ---------- ####
