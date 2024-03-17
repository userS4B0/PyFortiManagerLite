from sys import stderr
from pathlib import Path
from datetime import datetime
# from functools import reduce

from handlers.file_management import load_inventory, load_configuration
from functionality.Backup import Backup, BackupFailedError
from ui.cli import load_cli
from ui.interactive import load_interactive_menu
from ui.Logger import CustomLogger

DATE = datetime.now().strftime('%Y-%m-%d')      # Today's date in the format yyyy-mm-dd

logger = CustomLogger()
def main():
  
  #### TESTING AREA
  
  args = load_cli()

  if args.interactive: load_interactive_menu()
    
  else:
    if args.verbose: logger.set_verbosity(True)

    print (f'Selected args: {args}')
    
    try:
      config = load_configuration() # Load app configuration
      fortigates = load_inventory(Path(config['INVENTORY_FILE']))  # Load fortigate inventory

    except Exception as e:
      logger.critical(e)
      exit(1)

    for device in fortigates:
      # Load a Backup instance for every fortigate:

      try:
        backup = Backup(device)
        logger.log(f'Starting Job on: [{device.get_name()}]')
        backup.perform_backup(Path(config['BACKUP_PATH']), f'{device.get_name()}_bkp_{DATE}.conf')
        logger.log(f'Job completed in [{device.get_name()}] backup successfully saved in: {config['BACKUP_PATH']}')

      except BackupFailedError as e:
        logger.warn(e)
        pass

      except Exception as e:
          logger.critical(e)
          exit(1)    

if __name__ == '__main__':
  main()