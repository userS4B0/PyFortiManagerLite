from sys import stderr

from handlers import file_management
from api.FortiGate import FortiGate
from functionality.Backup import Backup, BackupFailedError

def main():
  
  # Load fortigate inventory
  print("Loading Inventory")
  try:
    devices = file_management.load_inventory()
    print("Inventory Loaded")
  
  except Exception as e:
    print(f'Error: {e}')
    print("Ending program...")
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
      backup.perform_backup(file_management.config['BACKUP_PATH']) # FIXME: Premision denied when accesing folder
      print(f'Job completed in [{device.get_name()}] backup successfully saved in: {file_management.config['BACKUP_PATH']}')

    except BackupFailedError as e:
      print(e, file=stderr)
      pass

    except Exception as e:
        print(e, file=stderr)
        exit(1)
  
  
  print("Program ended")
if __name__ == '__main__':
  main()