# File: /src/api_handlers.py

### IMPORTS
import requests

### GLOBAL VARS
# The req object is used to make https requests
req = requests.session()

# Comment these two lines below to enable SSL certificate warnings
requests.packages.urllib3.disable_warnings()
req.verify = False

online_ip = '',''

### FUNCTIONS
def ping(ip):

    # Do a simple request to the Fortigate to check if it is online
    try:
        req.get(f'https://{ip}', timeout=3)
        return True
    except:
        return False

def check_online_ip(fgt):

    # Access the global variable online_ip
    global online_ip

    # Check if the Fortigate is online on primary IP
    if ping(fgt['ip_1']):
        online_ip = fgt['ip_1']
        return online_ip
    
    # If not, check if the Fortigate has a secondary IP and if it is online
    elif fgt['ip_2'] != '' and ping(fgt['ip_2']):
        online_ip = fgt['ip_2']
        return online_ip
    
    # If the Fortigate is not available on any IP, return False
    online_ip = ''
    return False

def mount_url(fgt):

    # URI to backup the Fortigate
    URI = f'/api/v2/monitor/system/config/backup?scope={fgt["vdomtype"]}&access_token='

    # Check if the Fortigate is online on both IPs
    is_online = check_online_ip(fgt)
    if is_online:
        # If it is online, mount the URL to backup the Fortigate
        return f'https://{is_online}{URI}{fgt["token"]}'
    else:
        return ''

#### ---------- EOF ---------- ####