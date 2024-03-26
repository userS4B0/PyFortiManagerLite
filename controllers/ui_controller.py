# File: controller/ui_controller.py


import argparse
from pathlib import Path

from controllers.func.backup_payload import Backup, BackupFailedError
from controllers.logger_controller import DATE, CustomLogger, LogFileError
from models.fortigate_model import FortigateOfflineError
from views.ui_view import PAYLOADS, UIView


class UIController:
    """Controller class responsible for user interface interaction."""

    logger = CustomLogger()
    DEF_SEPARATOR_LENGTH = 80

    @staticmethod
    def load_cli() -> None:
        """Parses command line arguments."""
        parser = argparse.ArgumentParser(
            prog="PyFGTManagerLite",
            description="Executes defined payloads to FortiGate devices",
        )

        # Define command line arguments
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

        parser.add_argument("--verbose", "-v", action="store_true", default=False)
        parser.add_argument("--version", action="version", version="%(prog)s 0.2")

        return parser.parse_args()

    @staticmethod
    def cli_mode(inventory: dict, config: Path, log_file: Path, payload=None) -> None:
        """Loads program in CLI mode."""
        if payload is not None:
            match payload:
                case "single-backup":
                    print("Single Backup Functionality Coming Soon!")

                case "multi-backup":
                    for device in inventory:
                        try:
                            backup = Backup(device)
                            UIController.logger.info(
                                f"Starting Job on: [{device.get_name()}]", log_file
                            )
                            backup.perform_backup(
                                Path(config["BACKUP_PATH"]),
                                f"{device.get_name()}_bkp_{DATE}.conf",
                            )
                            UIController.logger.info(
                                f'Job completed in [{device.get_name()}] backup successfully saved in: {config['BACKUP_PATH']}',
                                log_file,
                            )

                        except LogFileError as e:
                            UIController.logger.warning(e)
                            pass

                        except BackupFailedError as e:
                            UIController.logger.warning(e, log_file)
                            pass

                        except Exception as e:
                            UIController.logger.critical(e, log_file)
                            exit(1)

                case "sync-objects":
                    print("Single Backup Functionality Coming Soon!")

                case "scrape-data":
                    print("Single Backup Functionality Coming Soon!")

                case _:
                    print("Invalid payload! try '--help' for payload information")

        else:
            print("No payload selected! try '--help' for payload information")

    @staticmethod
    def interactive_mode(inventory: dict, config: Path, log_file: Path) -> None:
        """Loads program in Interactive mode."""
        UIView.print_banner()

        program_running = True

        while program_running:
            UIView.print_menu()
            option = input("Choose an OPTION: ")

            match option:
                case "1":
                    UIController.show_inventory(inventory)
                case "2":
                    UIController.check_connectivity(inventory, log_file)
                case "3":
                    UIController.payload_menu(inventory, config, log_file)
                case "4":
                    UIView.clear_terminal()
                    print("Settings customization coming soon!")

                case "5":
                    UIView.clear_terminal()
                    print("Selected option 5, exiting program")
                    program_running = False
                    exit(0)

                case _:
                    UIView.clear_terminal()
                    print("Option not valid!")

    @staticmethod
    def show_inventory(inventory: dict) -> None:
        """Display Fortigate inventory."""
        UIView.clear_terminal()
        print("FORTIGATE INVENTORY")
        UIView.print_separator(UIController.DEF_SEPARATOR_LENGTH)

        for device in inventory:
            print(str(device))

        UIView.print_separator(UIController.DEF_SEPARATOR_LENGTH)
        UIView.pause_flow()

    @staticmethod
    def check_connectivity(inventory: dict, log_file: Path) -> None:
        """Check connectivity of Fortigate devices."""
        UIView.clear_terminal()
        print("CONNECTIVITY CHECK")
        UIView.print_separator(UIController.DEF_SEPARATOR_LENGTH)

        for device in inventory:
            try:
                access_ip = device.get_access_ip()
                UIController.logger.info(
                    f"[{device.get_name()}] Device connected at {access_ip}", log_file
                )
            except FortigateOfflineError as e:
                UIController.logger.warning(
                    f"FortiGate {device.get_name()} is offline: {e}", log_file
                )

        UIView.print_separator(UIController.DEF_SEPARATOR_LENGTH)
        UIView.pause_flow()

    @staticmethod
    def execute_payload(
        selected_payload: str, inventory: dict, config_file: Path, log_file: Path
    ) -> None:
        """Execute selected payload."""
        UIView.clear_terminal()
        print(f"Choosen payload: {PAYLOADS[selected_payload]}")

        match selected_payload:
            case "1":
                print(f"{PAYLOADS[selected_payload]} functionality Coming Soon!")
            case "2":
                for device in inventory:
                    try:
                        backup = Backup(device)
                        UIController.logger.info(
                            f"Starting Job on: [{device.get_name()}]", log_file
                        )
                        backup.perform_backup(
                            Path(config_file["BACKUP_PATH"]),
                            f"{device.get_name()}_bkp_{DATE}.conf",
                        )
                        UIController.logger.info(
                            f'Job completed in [{device.get_name()}] backup successfully saved in: {config_file['BACKUP_PATH']}',
                            log_file,
                        )
                    except Exception as e:
                        UIController.logger.warning(
                            f"Backup failed for {device.get_name()}: {e}", log_file
                        )
            case "3":
                print(f"{PAYLOADS[selected_payload]} functionality Coming Soon!")
            case "4":
                print(f"{PAYLOADS[selected_payload]} functionality Coming Soon!")

            case _:
                print("Invalid payload")

        UIView.pause_flow()
        UIView.clear_terminal()

    @staticmethod
    def payload_menu(inventory: dict, config_file: Path, log_file: Path) -> None:
        """Displays the payload menu."""
        payloads_menu_running = True
        while payloads_menu_running:
            UIView.clear_terminal()
            UIView.print_payloads_menu()
            payload_option = input("Choose a payload to execute: ")

            try:
                match payload_option:
                    case p if p in PAYLOADS:
                        UIController.execute_payload(
                            p, inventory, config_file, log_file
                        )

                    case "5":
                        UIView.clear_terminal()
                        payloads_menu_running = False
                    case "6":
                        UIView.clear_terminal()
                        print("Selected option 6, exiting program")
                        payloads_menu_running = False
                        exit(0)
                    case _:
                        UIView.clear_terminal()
                        print("Option not valid!")
            except FortigateOfflineError as e:
                print(f"Fortigate is offline: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
