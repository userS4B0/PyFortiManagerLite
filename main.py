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
    log_file = logging.create_log()
    log_file.write(logging.log("program started"))

    # Backup each Fortigate
    for fgt in inventory:

        # Clear error_message variable before each backup
        file.error_message
        error_message = ''
        
        print('\n========================================')
        print(f'Fortigate: {fgt["name"]}')
        log_file.write(logging.log(f'starting job on fgt_device_name_[{fgt["name"]}]'))
        
        # Call the main backup function
        bkp_ok = payloads.execute_backup(fgt)

        # Check if the backup was successful
        if bkp_ok:
            print('Backup successful!')
            log_file.write(logging.log(f'fgt_device_name_[{fgt["name"]}] at mgmt_ip_[{api.online_ip}]'))
            log_file.write(logging.log(f'fgt_device_name_[{fgt["name"]}] backup succesfull'))

        # If not, check if the Fortigate is offline or if there was an error
        else:
            if api.online_ip == '':
                print('Fortigate offline!')
                log_file.write(logging.log_error(f'fgt_device_name_[{fgt["name"]}] device is offline'))

            elif error_message != '':
                print(f'Error message: {file.error_message}')
                log_file.write(logging.log_error(f'fgt_device_name_[{fgt["name"]}] {file.error_message}'))

            print('Backup failed!')
            log_file.write(logging.log_error(f'fgt_device_name_[{fgt["name"]}] backup failed'))

        print('========================================\n')
    
    # Print the list of failed backups if there are any
    if len(bkp_fail) > 0:
        print('List of failed backups:')
        log_file.write(logging.log(f'fgt_device_name_[{fgt["name"]}]'))
        for fgt in bkp_fail:
            print(fgt)
            log_file.write(logging.log(f'{fgt}\n'))
        
        print(f'\nCount: {len(bkp_fail)}\n')
        log_file.write(logging.log(f'fgt_total_backup_count [{len(bkp_fail)}]'))

    log_file.write(logging.log("program ended"))
    log_file.close()
    print('Job finished!')
    sys.exit()

if __name__ == '__main__':
    main()
