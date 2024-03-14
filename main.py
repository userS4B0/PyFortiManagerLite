import sys

# Importing custom modules
from src import file_handlers as file
from src import api_handlers as api
from payloads import backup

bkp_fail = []  # List to store failed backups


def main():
    """
    Main function to execute the backup process for Fortigate devices.
    """
    inventory = file.read_inventory()   # Read the fortigates.csv file to get the list of devices
    file.create_folders()   # Create necessary folders for backups and logs if they don't exist
    
    file.logger.info('Program started') # Log program start

    # Backup each Fortigate device
    for fgt in inventory:
        file.error_message = '' # Clear error_message variable before each backup attempt 

        print('\n========================================')
        print(f'Fortigate: {fgt["Name"]}')
        
        file.logger.info(f'Starting Job at [{fgt["Name"]}]')

        bkp_file = backup.execute_backup(fgt)   # Call the backup function for the current Fortigate

        # Check if the backup was successful
        if bkp_file:
            print('Backup successful!')
            file.logger.info(f'Fortigate Name: [{fgt["Name"]}] at Management IP [{api.online_ip}] Backup Succesfull!')
        else:
            # If not successful, check if the Fortigate is offline or if there was an error
            if api.online_ip == '':
                print('Fortigate offline!')
                file.logger.warning(f'Fortigate Name: [{fgt["Name"]}] Is Offline!')
            
            elif file.error_message != '':
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
