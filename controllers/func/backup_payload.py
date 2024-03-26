import os
from pathlib import Path

import requests

from models.fortigate_model import FortiGate, FortigateOfflineError


class BackupFailedError(Exception):
    """Custom exception indicating that the backup job failed."""

    pass


class Backup:
    def __init__(self, fortigate: FortiGate):
        """
        Initialize the Backup object with a FortiGate instance.

        Parameters:
            fortigate (FortiGate): An instance of the FortiGate class representing the FortiGate device.
        """
        self.fortigate = fortigate

    def perform_backup(self, backup_path: Path, backup_name: str):
        """
        Perform a backup operation and save the backup file to the specified path.

        Parameters:
            backup_path (Path): The path where the backup file will be saved.
            backup_name (str): The name of the backup file.

        Raises:
            BackupFailedError: If the backup process fails for any reason.
        """
        req = requests.session()  # Create a session for HTTP requests

        # Handle SSL Self Signed Certificate validations
        if self.fortigate.has_s_signed_cert():
            requests.packages.urllib3.disable_warnings()
            req.verify = False

        try:
            backup_url = self.fortigate.mount_api_url()  # Mount the backup URL

            response = req.get(backup_url)  # Request backup via HTTP
            response.raise_for_status()  # Raise exception if status code is not successful

            full_path = backup_path / backup_name  # Mount full backup path

            # Write FortiGate config to file
            with open(full_path, "wb") as f:
                for line in response:
                    f.write(line)

            # Check if the file is a valid FortiGate config file
            with open(full_path, "r") as file:
                first_line = file.readline()
                if not first_line.startswith("#config"):
                    os.remove(full_path)  # Delete file
                    raise BackupFailedError("backup job failed, invalid backup file")

        except requests.RequestException as e:
            raise BackupFailedError(f"backup job failed due to HTTP error: {e}")

        except FortigateOfflineError as e:
            raise BackupFailedError(
                f"backup job failed, Fortigate is not connected: {e}"
            )

        except Exception as e:
            raise BackupFailedError(f"backup job failed: {e}")
