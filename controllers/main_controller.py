from pathlib import Path

from controllers.cli_controller import load_cli
from handlers.payloads.backup_payload import Backup, BackupFailedError
from controllers.interactive_controller import (
    load_main_menu,
    load_payloads_menu,
    pause_flow,
)
from controllers.logger_controller import DATE, CustomLogger, LogFileError
from handlers.file_management import load_configuration, load_inventory
from models.fortigate_model import FortigateOfflineError
from views.main_view import PAYLOADS, clear_terminal, load_banner, separator

logger = CustomLogger()


def main():
    args = load_cli()

    try:
        config = load_configuration()  # Load app configuration
        fortigates = load_inventory(
            Path(config["INVENTORY_FILE"])
        )  # Load FortiGate inventory
        log_file = Path(config["LOGS_PATH"]) / f"pyfgtmgrl_{DATE}.log"

    except LogFileError as e:
        logger.warning(e)
        log_file = None
        pass

    except Exception as e:
        logger.critical(e)
        exit(1)

    if args.interactive:
        logger.set_verbosity(True)
        try:
            load_banner()
            program_running = True
            while program_running:
                option = load_main_menu()

                match option:
                    case "1":
                        clear_terminal()

                        print("FORTIGATE INVENTORY")
                        separator(80)

                        for device in fortigates:
                            print(
                                f"|   {device.get_name()}   |   {device.get_management_ip_01()}   |   {device.get_management_ip_02()}   |   {device.get_vdom_type()}   |"
                            )

                        separator(80)

                        pause_flow()

                    case "2":
                        print("CONNECTIVITY CHECK")
                        separator(80)

                        for device in fortigates:
                            try:
                                logger.info(
                                    f"Testing connectivity to: [{device.get_name()}] on [{device.get_management_ip_01()}] & [{device.get_management_ip_02()}]",
                                    log_file,
                                )
                                access_ip = device.get_access_ip()
                                logger.info(f"Device connected at {access_ip}")

                            except LogFileError as e:
                                logger.warning(e)
                                pass

                            except FortigateOfflineError as e:
                                logger.warning(e, log_file)
                                pass

                        separator(80)

                        pause_flow()

                    case "3":
                        clear_terminal()
                        payload_menu_running = True
                        while payload_menu_running:
                            payload_option = load_payloads_menu()

                            match payload_option:
                                case "1":
                                    clear_terminal()
                                    print(
                                        f"Choosen payload: {PAYLOADS[payload_option]}"
                                    )
                                    print(
                                        f"{PAYLOADS[payload_option]} functionality Coming Soon!"
                                    )
                                    pause_flow()

                                case "2":
                                    clear_terminal()
                                    print(
                                        f"Choosen payload: {PAYLOADS[payload_option]}"
                                    )

                                    for device in fortigates:
                                        try:
                                            backup = Backup(device)
                                            logger.info(
                                                f"Starting Job on: [{device.get_name()}]",
                                                log_file,
                                            )
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

                                    pause_flow()
                                    clear_terminal()

                                case "3":
                                    clear_terminal()
                                    print(
                                        f"Choosen payload: {PAYLOADS[payload_option]}"
                                    )
                                    print(
                                        f"{PAYLOADS[payload_option]} functionality Coming Soon!"
                                    )
                                    pause_flow()

                                case "4":
                                    clear_terminal()
                                    print(
                                        f"Choosen payload: {PAYLOADS[payload_option]}"
                                    )
                                    print(
                                        f"{PAYLOADS[payload_option]} functionality Coming Soon!"
                                    )
                                    pause_flow()

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
        except KeyboardInterrupt:
            print("\nKeyboard interruption! Exiting...")
            exit(0)

    elif args.verbose:
        logger.set_verbosity(True)

    try:
        selected_payload = args.payload

        if selected_payload is not None:
            match selected_payload:
                case "single-backup":
                    print("Single Backup Functionality Coming Soon!")

                case "multi-backup":
                    for device in fortigates:
                        try:
                            backup = Backup(device)
                            logger.info(
                                f"Starting Job on: [{device.get_name()}]", log_file
                            )
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
    except KeyboardInterrupt:
        print("\nKeyboard interruption! Exiting...")
        exit(0)


if __name__ == "__main__":
    main()
