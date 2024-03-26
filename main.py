from pathlib import Path

from controllers.file_controller import (
    DataLoadingError,
    load_configuration,
    load_inventory,
)
from controllers.logger_controller import DATE, LogFileError
from controllers.ui_controller import UIController


def main():
    args = UIController.load_cli()

    if args.verbose:
        UIController.logger.set_verbosity(True)
    try:
        config = load_configuration()  # Load app configuration
        fortigates = load_inventory(
            Path(config["INVENTORY_FILE"])
        )  # Load FortiGate inventory
        log_file = Path(config["LOGS_PATH"]) / f"pyfgtmgrl_{DATE}.log"

    except LogFileError as e:
        UIController.logger.warning(e)
        log_file = None
        pass

    except DataLoadingError as e:
        UIController.logger.critical(e)
        exit(1)

    except Exception as e:
        UIController.logger.critical(e)
        exit(1)

    try:
        if args.interactive:
            UIController.interactive_mode(fortigates, config, log_file)
        else:
            payload = args.payload
            UIController.cli_mode(fortigates, config, log_file, payload)
    except KeyboardInterrupt:
        print("\nKeyboard Interruption Detected\nExiting Program...")
        exit(0)


if __name__ == "__main__":
    main()
