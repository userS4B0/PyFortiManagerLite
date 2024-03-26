from pathlib import Path

from controllers.cli_controller import load_cli
from controllers.interactive_controller import interactive_mode, logger
from controllers.logger_controller import DATE, LogFileError

from handlers.file_management import load_configuration, load_inventory

def main():
    args = load_cli()
    print(f'Selected Values: {args}')

    try:
        config = load_configuration()  # Load app configuration
        print(f"Config loaded at: {config}")
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
        print("Loading interactive menu...")
        interactive_mode(fortigates, config, log_file)


    # if args.verbose:
    #     logger.set_verbosity(True)

    # try:
    #     selected_payload = args.payload

    #     if selected_payload is not None:
    #         match selected_payload:
    #             case "single-backup":
    #                 print("Single Backup Functionality Coming Soon!")

    #             case "multi-backup":
    #                 for device in fortigates:
    #                     try:
    #                         backup = Backup(device)
    #                         logger.info(
    #                             f"Starting Job on: [{device.get_name()}]", log_file
    #                         )
    #                         backup.perform_backup(
    #                             Path(config["BACKUP_PATH"]),
    #                             f"{device.get_name()}_bkp_{DATE}.conf",
    #                         )
    #                         logger.info(
    #                             f'Job completed in [{device.get_name()}] backup successfully saved in: {config['BACKUP_PATH']}',
    #                             log_file,
    #                         )

    #                     except LogFileError as e:
    #                         logger.warning(e)
    #                         pass

    #                     except BackupFailedError as e:
    #                         logger.warning(e, log_file)
    #                         pass

    #                     except Exception as e:
    #                         logger.critical(e, log_file)
    #                         exit(1)

    #             case "sync-objects":
    #                 print("Single Backup Functionality Coming Soon!")

    #             case "scrape-data":
    #                 print("Single Backup Functionality Coming Soon!")

    #             case _:
    #                 print("Invalid payload! try '--help' for payload information")

    #     else:
    #         print("No payload selected! try '--help' for payload information")
    # except KeyboardInterrupt:
    #     print("\nKeyboard interruption! Exiting...")
    #     exit(0)

if __name__ == "__main__":
    main()
