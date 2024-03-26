from sys import stdout, stderr
from datetime import datetime

DATE = datetime.now().strftime('%Y-%m-%d')      # Today's date in the format yyyy-mm-dd
TIME = datetime.now().strftime('%H:%M:%S')      # Today's date in the format yyyy-mm-dd

class LogFileError(Exception):
    pass

class CustomLogger: # FIXME: Loggin file overwrites itself
  def __init__(self, verbosity=False):
    self.verbosity = verbosity

  def set_verbosity(self, verbosity: bool):
    self.verbosity = verbosity
  
  def info(self, message: str, file = None):
    if self.verbosity: print(f'INFO: {message}', file = stdout) 
    
    if file is not None:
      try:
        with open(file, 'a') as f:
            f.write(f'[{DATE}][{TIME}] INFO: {message}\n')

      except FileNotFoundError as e: raise LogFileError(f'log file not found: {e}')
      except Exception as e: raise LogFileError(f'error reading log file: {e}')  

  def warning(self, message: str, file = None):
    if self.verbosity: print(f'WARNING: {message}', file = stderr) 
    
    if file != None:
      try:
        with open(file, 'a') as f:
            f.write(f'[{DATE}][{TIME}] WARNING: {message}\n')

      except FileNotFoundError as e: raise LogFileError(f'log file not found: {e}')
      except Exception as e: raise LogFileError(f'error reading log file: {e}') 

  def error(self, message: str, file = None):
    if self.verbosity: print(f'ERROR: {message}', file = stderr) 
    
    if file != None:
      try:
        with open(file, 'a') as f:
            f.write(f'[{DATE}][{TIME}] ERROR: {message}\n')

      except FileNotFoundError as e: raise LogFileError(f'log file not found: {e}')
      except Exception as e: raise LogFileError(f'error reading log file: {e}')    

  def critical(self, message: str, file = None):    
    if self.verbosity: print(f'CRITICAL: {message}', file = stderr) 
    
    if file != None:
      try:
        with open(file, 'a') as f:
            f.write(f'[{DATE}][{TIME}] CRITICAL: {message}\n')

      except FileNotFoundError as e: raise LogFileError(f'log file not found: {e}')
      except Exception as e: raise LogFileError(f'error reading log file: {e}')    
