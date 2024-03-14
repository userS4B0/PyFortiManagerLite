import sys

from src import file_handlers as file
from src import api_handlers as api

import payloads
from payloads import backup

bkp_fail = []

def main():

    # Read the fortigates.csv file
    inventory = file.read_inventory()
    
    # Create folders for backups and logs if they don't exist
    file.create_folders()

    file.logger.info('Program started')

    # Backup each Fortigate
    for fgt in inventory:

        # Clear error_message variable before each backup
        file.error_message
        error_message = ''
        
        print('\n========================================')
        print(f'Fortigate: {fgt["Name"]}')
        file.logger.info(f'Starting Job at [{fgt["Name"]}]')
        
        # Call the main backup function
        
        # FIXME: Doesnt read the bkp file correctly
        # payloads.collect.retrieve_data(fgt)
        # bkp_file = payloads.backup.execute_backup(fgt)

        bkp_file = backup.execute_backup(fgt)
        
        # Check if the backup was successful
        if bkp_file:
            print('Backup successful!')
            file.logger.info(f'Fortigate Name: [{fgt["Name"]}] at Management IP [{api.online_ip}] Backup Succesfull!')

        # If not, check if the Fortigate is offline or if there was an error
        else:
            if api.online_ip == '':
                print('Fortigate offline!')
                file.logger.warning(f'Fortigate Name: [{fgt["Name"]}] Is Offline!')

            elif error_message != '':
                print(f'Error message: {file.error_message}')
                file.logger.error(f'Fortigate Name: [{fgt["Name"]}]; {file.error_message}')

            print('Backup failed!')
            file.logger.warning(f'Fortigate Name: [{fgt["Name"]}] Backup Failed!')

        print('========================================\n')
    
    # Print the list of failed backups if there are any
    if len(bkp_fail) > 0:
        print('List of failed backups:')
        file.logger.warning(f'List of failed backups:')
        file.logger.warning(f'Fortigate Name: [{fgt["Name"]}]')
        
        for fgt in bkp_fail:
            print(fgt)
            file.logger.warning(f'{fgt}')
        
        print(f'\nCount: {len(bkp_fail)}\n')
        file.logger.warning(f'Total of Failed Backups [{len(bkp_fail)}]')

    print('Job finished!')
    file.logger.info('Program ended')
    sys.exit()

if __name__ == '__main__':
    main()
