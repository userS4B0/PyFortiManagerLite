# File: /src/log_handlers.py

### IMPORTS
import os
import sys
from src import file_handlers as fh
### GLOBAL VARS

### FUNCTIONS
def create_log():
    
    try:
        # Create log file and remain it open to write
        return open(os.path.join(fh.LOGS_FOLDER, f'bkp-{fh.DATE}.log'), 'a')
    except Exception as e:
        print(f'Error creating the log file: {e}')
        input('Press ENTER to exit...')
        sys.exit()
        
#### ---------- EOF ---------- ####
