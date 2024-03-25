import yaml
import csv

from pathlib import Path
from api.Fortigate import FortiGate

class ConfigurationError (Exception):
  """Custom exception for configuration errors."""
  pass

class DataLoadingError (Exception):
  """Custom exception for data loading errors."""
  pass

def read_yaml_config(config_file: Path):
  """
    Reads a YAML configuration file.

    Args:
        config_file (Path): Path to the YAML configuration file.

    Returns:
        dict: Dictionary containing the YAML data.

    Raises:
        ConfigurationError: If an error occurs while reading or parsing the configuration file.
    """
  try:
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config
  except FileNotFoundError as e:
    raise ConfigurationError(f'config file not found: {e}')
  except Exception as e:
    raise ConfigurationError(f'error loading config files: {e}')

def load_configuration():
  """
  Load configuration from YAML file.
  
  Returns:
      dict: Configuration data.
  
  Raises:
      ConfigurationError: If an error occurs while loading the configuration data.
  """
  # CONFIG_PATH = Path('.').parent / 'config.yaml'  # Set the path to the configuration file
  CONFIG_PATH = Path('.').parent / 'user_config.yaml'  # TODO: ONLY PRE ENVIROMENT
  
  try:
    
    user_config = read_yaml_config (CONFIG_PATH)
    return user_config
      
  except Exception as e:
    raise DataLoadingError(f'error loading program data: {e}')

def load_inventory(inventory_file: Path):
    """
    Load inventory data from a CSV file.

    Args:
        inventory_file (Path): Path to the inventory CSV file.

    Returns:
        list: List of dictionaries containing inventory data.

    Raises:
        DataLoadingError: If an error occurs while loading the inventory data.
    """
    try:
        with open(inventory_file, 'r') as file:
            
            inventory = map(lambda fortigate: FortiGate(
              fortigate['Name'], 
              fortigate['Managment IP 01'], 
              fortigate['Managment IP 02'], 
              fortigate['VDOM Type'], 
              fortigate['SelfSignedCertificate'], 
              fortigate['API Token']), 
                            list(csv.DictReader(file, delimiter=','))
            )
            
            return inventory
      
    except FileNotFoundError as e:
      raise DataLoadingError(f'inventory not found: {e}')
    
    except Exception as e:
      raise DataLoadingError(f'error reading inventory file: {e}')