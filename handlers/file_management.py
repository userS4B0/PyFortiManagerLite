import yaml, csv

from pathlib import Path

CURRENT_DIR = Path('.')
APP_DIR = CURRENT_DIR.parent
DEFAULT_CONFIG_PATH = APP_DIR / 'data' / 'config.yaml'
# USER_CONFIG_PATH = APP_DIR / 'user_config.yaml'

class ConfigurationError (Exception):
  pass

class DataLoadingError (Exception):
  pass

def read_yaml_config(config_file: Path):
  try:
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config
  except FileNotFoundError as e:
    raise ConfigurationError(f'Configuration file not found: {e}')
  except Exception as e:
    raise ConfigurationError(f'Error loading config files: {e}')

def load_configuration():
  try:
    # default_config = read_yaml_config(DEFAULT_CONFIG_PATH)
    user_config = read_yaml_config (USER_CONFIG_PATH)

    # final_config = {}
    # for key, value in default_config.items():
    #     if key in user_config and user_config[key] is not None:
    #         final_config[key] = user_config[key]
    #     else:
    #         final_config[key] = value

    #     return final_config
    return user_config
      
  except Exception as e:
    raise DataLoadingError(f'Error loading program data: {e}')

def load_inventory(inventory_file: Path):

    try:
        with open(inventory_file, 'r') as file:
            inventory = list(csv.DictReader(file, delimiter=','))
        return inventory
      
    except FileNotFoundError as e:
      raise DataLoadingError(f'Inventory not found: {e}')
    
    except Exception as e:
      raise DataLoadingError(f'Error reading inventory.csv file: {e}')