from sys import stdout, stderr



class CustomLogger:
  def __init__(self, verbosity=False):
    self.verbosity = verbosity

    # self.format = '%(asctime)s - %(levelname)s - %(message)s'
    self.format = '%(asctime)s - %(message)s'

  def set_verbosity(self, verbosity: bool):
    self.verbosity = verbosity
  
  def log(self, message: str, file = stdout):
    if self.verbosity:
      print(f'INFO: {message}', file = file)

  def warn(self, message: str, file = stderr):
    if self.verbosity:
      print(f'WARNING: {message}', file = file)    

  def error(self, message: str, file = stderr):
      print(f'ERROR: {message}', file = file)    

  def critical(self, message: str, file = stderr):
    print(f'CRITICAL: {message}', file = file)    
