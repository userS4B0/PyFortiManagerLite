import os
import yaml

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(APP_DIR, 'data')
DEFAULT_CONFIG_PATH = os.path.join(DATA_DIR, 'config', 'config.yaml')
USER_CONFIG_PATH = os.path.join(DATA_DIR, 'config', 'user_config.yaml')

# # Initial Tests
# print(CURRENT_DIR)
# print(APP_DIR)
# print(DATA_DIR)
# print(CONFIG_PATH)

def read_yaml_config(file_path):  # TODO: make it inherent from SO
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def get_final_config():
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
# Imprime la configuración final
print("Final Configuration:")
config = get_final_config()
print(config)