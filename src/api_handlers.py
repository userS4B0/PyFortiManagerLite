# File: /src/api_handlers.py

### IMPORTS
import requests  # Importing the 'requests' module for making HTTP requests

from src.file_handlers import logger

### GLOBAL VARS
# The 'req' object is used to make HTTPS requests
req = requests.session()

# Disable SSL certificate warnings by setting 'verify' to False
requests.packages.urllib3.disable_warnings()
req.verify = False

# The 'online_ip' variable stores the IP address of the online FortiGate device
online_ip = '', ''

### FUNCTIONS
def ping(ip):
    """
    Checks if a FortiGate device is online by sending a simple request to it.

    Parameters:
    - ip (str): The IP address of the FortiGate device.

    Returns:
    - bool: True if the FortiGate responds within 3 seconds, False otherwise.
    """
    try:
        # Attempt to send a request to the FortiGate with a timeout of 3 seconds
        req.get(f'https://{ip}', timeout=3)
        return True
    except:
        return False

def check_online_ip(fgt):
    """
    Checks if the FortiGate device is online on any of its IP addresses.

    Parameters:
    - fgt (dict): A dictionary containing information about the FortiGate device,
                 including primary and secondary IP addresses.

    Returns:
    - str: The IP address of the online FortiGate device, if found.
    - False: If the FortiGate is not available on any IP address.
    """
    # Access the global variable 'online_ip'
    global online_ip

    # Check if the FortiGate is online on its primary IP address
    logger.info(f'Attempting request to {fgt['Managment IP 01']}')
    if ping(fgt['Managment IP 01']):
        online_ip = fgt['Managment IP 01']
        logger.info(f'{fgt['Managment IP 01']} is online')
        return online_ip
    
    # If not, check if the FortiGate has a secondary IP address and if it is online
    elif fgt['Managment IP 02'] != '' and ping(fgt['Managment IP 02']):
        logger.warning(f'{fgt['Managment IP 01']} connection timed out')
        logger.info(f'Attempting request to {fgt['Managment IP 02']}')
        logger.info(f'{fgt['Managment IP 02']} is online')
        online_ip = fgt['Managment IP 02']
        return online_ip
    
    # If the FortiGate is not available on any IP address, return False
    logger.warning(f'{fgt['Managment IP 02']} connection timed out')
    logger.error(f'There is no Management IP assigned')
    online_ip = ''
    return False

def mount_url(fgt):
    """
    Mounts the URL for backing up the FortiGate device.

    Parameters:
    - fgt (dict): A dictionary containing information about the FortiGate device,
                 including the VDOM type and access token.

    Returns:
    - str: The URL for backing up the FortiGate device.
    - '': If the FortiGate is not available on any IP address.
    """
    # URI to backup the FortiGate
    URI = f'/api/v2/monitor/system/config/backup?scope={fgt["VDOM Type"]}&access_token='

    # Check if the FortiGate is online on any of its IP addresses
    is_online = check_online_ip(fgt)
    if is_online:
        # If it is online, mount the URL to backup the FortiGate
        logger.info(f'Mounted URL at https://{is_online}{URI}{fgt["API Token"]}')
        return f'https://{is_online}{URI}{fgt["API Token"]}'
    else:
        logger.warning(f'No URL is mounted')
        return ''

#### ---------- EOF ---------- ####
