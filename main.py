import sys

from src import file_handlers as file
from src import log_handlers as logging
from src import api_handlers as api
from src import payloads

bkp_fail = []

def main():

    # Read the fortigates.csv file
    inventory = file.read_inventory()
    
    # Create folders for backups and logs if they don't exist
    file.create_folders()

    # Create log file
    log = logging.create_log()
    log.write(f'Backup log - {file.DATE}\n')

    # Backup each Fortigate
    for fgt in inventory:

        # Clear error_message variable before each backup
        file.error_message
        error_message = ''
        
        print('\n========================================')
        print(f'Fortigate: {fgt["name"]}')

        log.write('\n========================================\n')
        log.write(f'Fortigate: {fgt["name"]}\n')
        
        # Call the main backup function
        bkp_ok = payloads.execute_backup(fgt)

        # Check if the backup was successful
        if bkp_ok:
            print('Backup successful!')
            log.write(f'Fortigate online on IP: {api.online_ip}\n')
            log.write('Backup successful!\n')

        # If not, check if the Fortigate is offline or if there was an error
        else:
            if api.online_ip == '':
                print('Fortigate offline!')
                log.write('Fortigate offline!\n')

            elif error_message != '':
                print(f'Error message: {error_message}')
                log.write(f'Error message: {error_message}\n')

            print('Backup failed!')
            log.write('Backup failed!\n')
            bkp_fail.append(fgt['name'])

        print('========================================\n')
        log.write('========================================\n')
    
    # Print the list of failed backups if there are any
    if len(bkp_fail) > 0:
        print('List of failed backups:')
        log.write('\nList of failed backups:\n')
        for fgt in bkp_fail:
            print(fgt)
            log.write(f'{fgt}\n')
        
        print(f'\nCount: {len(bkp_fail)}\n')
        log.write(f'\nCount: {len(bkp_fail)}\n')

    log.close()
    print('Backup finished!')
    sys.exit()

if __name__ == '__main__':
    main()
