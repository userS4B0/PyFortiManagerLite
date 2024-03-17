import argparse

def load_cli():
  
  # Program definition
  parser = argparse.ArgumentParser(
                    prog='PyFGTManagerLite',
                    description='Executes defined payloads to FortiGate devices')
  
  # Arguments
  parser.add_argument('--interactive', '-i',
                      required = False,
                      action = 'store_true',
                      default = False,
                      help = 'Loads an interactive shell for the user to select defined actions to perform.')
  
  parser.add_argument('--payload', '-p', 
                      required = False,
                      help = 'Expects a defined payload to execute.')
  
  parser.add_argument('--notify', '-n', 
                      required = False, 
                      action = 'store_true', 
                      default = False , 
                      help = 'Either notifies to the contact list established in the config file or performs the selected actions without notifying.')
  
  parser.add_argument('--verbose', '-v', action='store_true', default=False)
  parser.add_argument('--version', action='version', version='%(prog)s 0.2')

  
  return parser.parse_args()