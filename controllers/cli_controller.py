import argparse


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