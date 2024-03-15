import os
import yaml
import csv

from pathlib import Path

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(APP_DIR, 'data')
DEFAULT_CONFIG_PATH = os.path.join(APP_DIR, 'config', 'config.yaml')
USER_CONFIG_PATH = os.path.join(APP_DIR, 'config', 'user_config.yaml')

class DataLoadingError (Exception):
  pass

def read_yaml_config(file_path):  # TODO: make it inherent from SO
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_configuration():
  default_config = read_yaml_config(DEFAULT_CONFIG_PATH)
  user_config = read_yaml_config (USER_CONFIG_PATH)

  # Crea un diccionario en base a los 2 especificados en el fichero de configuración
  # de lo contrario, utiliza la configuración por defecto
  final_config = {}
  for key, value in default_config.items():
      if key in user_config and user_config[key] is not None:
          final_config[key] = user_config[key]
      else:
          final_config[key] = value

  return final_config

config = load_configuration()

def load_inventory():
    """
    Reads the inventory data from the 'inventory.csv' file.

    Returns:
        list: A list of dictionaries containing information about the FortiGate devices.
    """
    try:
        with open(os.path.join(config['INVENTORY_FILE']), 'r') as file:
            inventory = list(csv.DictReader(file, delimiter=','))
        return inventory
      
    except FileNotFoundError as e:
      raise DataLoadingError(f'Inventory not found: {e}')
    
    except Exception as e:
      raise DataLoadingError(f'Error reading inventory.csv file: {e}')

def load_registry():
    """
    Reads the inventory data from the 'registry.csv' file.

    Returns:
        list: A list of dictionaries containing information about the FortiGate devices.
    """
    try:
        with open(os.path.join(config['REGISTRY_FILE']), 'r') as file:
            inventory = list(csv.DictReader(file, delimiter=','))
        return inventory
      
    except FileNotFoundError as e:
      raise DataLoadingError(f'Registry not found: {e}')
    
    except Exception as e:
      raise DataLoadingError(f'Error reading registry.csv file: {e}')