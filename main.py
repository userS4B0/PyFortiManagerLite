from pathlib import Path

from controllers.logger_controller import DATE, LogFileError
from controllers.ui_controller import cli_mode, interactive_mode, load_cli, logger
from controllers.file_controller import (
    DataLoadingError,
    load_configuration,
    load_inventory,
)


def main():
    args = load_cli()

    if args.verbose:
        logger.set_verbosity(True)
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

    except DataLoadingError as e:
        logger.critical(e)
        exit(1)

    except Exception as e:
        logger.critical(e)
        exit(1)

    try:
        if args.interactive:
            interactive_mode(fortigates, config, log_file)
        else:
            selected_payload = args.payload
            cli_mode(fortigates, config, log_file, selected_payload)
    except KeyboardInterrupt:
        print("\nKeyboard Interruption Detected\nExiting Program...")
        exit(0)


if __name__ == "__main__":
    main()
