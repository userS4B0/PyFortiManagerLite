from sys import stderr
from pathlib import Path
# from functools import reduce

from handlers.file_management import load_inventory, load_configuration
from functionality.Backup import Backup, BackupFailedError
from ui.cli import load_cli
from ui.interactive import load_interactive_menu
from ui.Logger import CustomLogger, LogFileError, DATE

logger = CustomLogger()
def main():
  args = load_cli()

  try:
    config = load_configuration() # Load app configuration
    fortigates = load_inventory(Path(config['INVENTORY_FILE']))  # Load fortigate inventory
    log_file = Path(config['LOGS_PATH']) / f'pyfgtmgrl_{DATE}.log'

  except LogFileError as e: 
    logger.warning(e)
    log_file = None
    pass

  except Exception as e:
    logger.critical(e)
    exit(1)

  if args.interactive: load_interactive_menu()
  if args.verbose: logger.set_verbosity(True)

  print (f'Selected args: {args}')
    
  for device in fortigates:
    # Load a Backup instance for every fortigate:

    try:
      backup = Backup(device)
      logger.info(f'Starting Job on: [{device.get_name()}]', log_file)
      backup.perform_backup(Path(config['BACKUP_PATH']), f'{device.get_name()}_bkp_{DATE}.conf')
      logger.info(f'Job completed in [{device.get_name()}] backup successfully saved in: {config['BACKUP_PATH']}', log_file)

    except LogFileError as e: 
      logger.warning(e)
      pass
    
    except BackupFailedError as e:
      logger.warning(e, log_file)
      pass
    
    except Exception as e:
      logger.critical(e, log_file)
      exit(1)    

if __name__ == '__main__':
  main()