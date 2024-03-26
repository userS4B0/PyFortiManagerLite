import argparse
from pathlib import Path

from controllers.logger_controller import DATE, CustomLogger, LogFileError
from controllers.func.backup_payload import Backup, BackupFailedError
from models.fortigate_model import FortigateOfflineError
from views.ui_view import (
    PAYLOADS,
    clear_terminal,
    load_banner,
    load_main_menu,
    load_payloads_menu,
    pause_flow,
    separator,
)


def load_cli():
    # Program definition
    parser = argparse.ArgumentParser(
        prog="PyFGTManagerLite",
        description="Executes defined payloads to FortiGate devices",
    )

    # Arguments
    parser.add_argument(
        "--interactive",
        "-i",
        required=False,
        action="store_true",
        default=False,
        help="Loads an interactive shell for the user to select defined actions to perform.",
    )

    parser.add_argument(
        "--payload",
        "-p",
        required=False,
        help="""
                      Expects a defined payload to execute.\n
                      List of avalible payloads:
                        - single-backup: attempts to perform a backup task via api throug a given Fortigate device from inventory.
                        - multi-backup: attempts to perform backup jobs for all fortigate devices in inventory.
                        - sync-objects: (Only in multi vdom fortigate devices) attempts to replicate and sync objects between fortigate devices vdoms.
                        - scrape-data: attempts to get data from a fortigate config file and loads it in registry.csv file.
                      """,
    )

    parser.add_argument(
        "--notify",
        "-n",
        required=False,
        action="store_true",
        default=False,
        help="Either notifies to the contact list established in the config file or performs the selected actions without notifying.",
    )

    parser.add_argument("--verbose", "-v", action="store_true", default=False)
    parser.add_argument("--version", action="version", version="%(prog)s 0.2")

    return parser.parse_args()


def cli_mode(fortigates, config, log_file, payload=None):
    if payload is not None:
        match payload:
            case "single-backup":
                print("Single Backup Functionality Coming Soon!")

            case "multi-backup":
                for device in fortigates:
                    try:
                        backup = Backup(device)
                        logger.info(f"Starting Job on: [{device.get_name()}]", log_file)
                        backup.perform_backup(
                            Path(config["BACKUP_PATH"]),
                            f"{device.get_name()}_bkp_{DATE}.conf",
                        )
                        logger.info(
                            f'Job completed in [{device.get_name()}] backup successfully saved in: {config['BACKUP_PATH']}',
                            log_file,
                        )

                    except LogFileError as e:
                        logger.warning(e)
                        pass

                    except BackupFailedError as e:
                        logger.warning(e, log_file)
                        pass

                    except Exception as e:
                        logger.critical(e, log_file)
                        exit(1)

            case "sync-objects":
                print("Single Backup Functionality Coming Soon!")

            case "scrape-data":
                print("Single Backup Functionality Coming Soon!")

            case _:
                print("Invalid payload! try '--help' for payload information")

    else:
        print("No payload selected! try '--help' for payload information")


logger = CustomLogger()


def show_inventory(inventory):
    clear_terminal()
    print("FORTIGATE INVENTORY")
    separator(80)

    for device in inventory:
        print(str(device))

    separator(80)
    pause_flow()


def check_connectivity(fortigates, log_file):
    clear_terminal()
    print("CONNECTIVITY CHECK")
    separator(80)

    for device in fortigates:
        try:
            access_ip = device.get_access_ip()
            logger.info(
                f"[{device.get_name()}] Device connected at {access_ip}", log_file
            )
        except FortigateOfflineError as e:
            logger.warning(f"FortiGate {device.get_name()} is offline: {e}", log_file)

    separator(80)
    pause_flow()


def execute_payload(selected_payload, fortigates, config_file, log_file):
    clear_terminal()
    print(f"Choosen payload: {PAYLOADS[selected_payload]} at id {selected_payload}")

    # Implement logic for each payload option
    match selected_payload:
        case "1":
            print(f"{PAYLOADS[selected_payload]} functionality Coming Soon!")
        case "2":
            for device in fortigates:
                try:
                    backup = Backup(device)
                    logger.info(f"Starting Job on: [{device.get_name()}]", log_file)
                    backup.perform_backup(
                        Path(config_file["BACKUP_PATH"]),
                        f"{device.get_name()}_bkp_{DATE}.conf",
                    )
                    logger.info(
                        f'Job completed in [{device.get_name()}] backup successfully saved in: {config_file['BACKUP_PATH']}',
                        log_file,
                    )
                except Exception as e:
                    logger.warning(
                        f"Backup failed for {device.get_name()}: {e}", log_file
                    )
        case "3":
            print(f"{PAYLOADS[selected_payload]} functionality Coming Soon!")
        case "4":
            print(f"{PAYLOADS[selected_payload]} functionality Coming Soon!")

        case _:
            print("Invalid payload")

    pause_flow()
    clear_terminal()


def interactive_mode(fortigates, config, log_file):
    load_banner()
    program_running = True
    while program_running:
        option = load_main_menu()

        match option:
            case "1":
                show_inventory(fortigates)
            case "2":
                check_connectivity(fortigates, log_file)
            case "3":
                payload_menu_running = True
                while payload_menu_running:
                    payload_option = load_payloads_menu()
                    if payload_option in PAYLOADS:
                        execute_payload(payload_option, fortigates, config, log_file)

                    match payload_option:
                        case "5":
                            clear_terminal()
                            payload_menu_running = False
                        case "6":
                            clear_terminal()
                            print("Selected option 6, exiting program")
                            program_running = False
                            exit(0)
                        case _:
                            clear_terminal()
                            print("Option not valid!")
            case "4":
                clear_terminal()
                print("Settings customization coming soon!")

            case "5":
                clear_terminal()
                print("Selected option 5, exiting program")
                program_running = False
                exit(0)

            case _:
                clear_terminal()
                print("Option not valid!")
