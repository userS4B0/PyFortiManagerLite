from sys import stderr
from pathlib import Path
from datetime import datetime

from handlers.file_management import load_inventory, load_configuration
from api.FortiGate import FortiGate
from functionality.Backup import Backup, BackupFailedError

DATE = datetime.now().strftime('%Y-%m-%d')      # Today's date in the format yyyy-mm-dd

def main():
  
  #### TESTING AREA
  
  # from handlers.file_management import CURRENT_DIR, APP_DIR, DEFAULT_CONFIG_PATH, USER_CONFIG_PATH
  
  # print(f' Current directory: {CURRENT_DIR.absolute()}')
  # print(f' App Directory: {APP_DIR.absolute()}')
  # print(f' Default Config Path: {DEFAULT_CONFIG_PATH.absolute()}')
  # print(f' User config path: {USER_CONFIG_PATH.absolute()}')
  
  try:
    print("Loading configuration")
    config = load_configuration() # Load app configuration
    print("Configuration loaded")
    print(config)
    
    print("Loading Inventory")
    devices = load_inventory(Path(config['INVENTORY_FILE']))  # Load fortigate inventory
    print("Inventory Loaded")
    
  except Exception as e:
    print(e, file=stderr)
    exit(1)
  
  # Convert devices into FortiGate instances in memory
  fortigates = []
  
  for device in devices:
    print(f'Loading device {device}')
    try:
      fortigate = FortiGate(
        device['Name'], 
        device['Managment IP 01'], 
        device['Managment IP 02'], 
        device['VDOM Type'], 
        device['SelfSignedCertificate'],
        device['API Token']
      )
      fortigates.append(fortigate)

    except Exception as e:
      print(e, file=stderr)
      exit(1)
      
  print('All devices loaded')
  print(fortigates)
  
  # Execute all backups
  for device in fortigates:
    # Load a Backup instance for every fortigate:
    try:
      backup = Backup(device)
      print(f'Starting Job on: [{device.get_name()}]')
      backup.perform_backup(Path(config['BACKUP_PATH']), f'{device.get_name()}_bkp_{DATE}.conf')
      print(f'Job completed in [{device.get_name()}] backup successfully saved in: {config['BACKUP_PATH']}')

    except BackupFailedError as e:
      print(e, file=stderr)
      pass

    except Exception as e:
        print(e, file=stderr)
        exit(1)
  
  
  print("Program ended")
if __name__ == '__main__':
  main()