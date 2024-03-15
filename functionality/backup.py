import requests

from api.FortiGate import FortiGate, FortigateOfflineError 

class BackupFailedError(Exception):
    """Custom exception indicating that the backup job failed."""
    pass

class Backup:
    def __init__(self, fortigate: FortiGate):
        """Initialize the Backup object with a FortiGate instance."""
        self.fortigate = fortigate

    def perform_backup(self, backup_path):
        """Perform a backup operation and save the backup file to the specified path."""
        
        req = requests.session()
        
        if self.fortigate.has_self_signed_certificate():
            requests.packages.urllib3.disable_warnings()
            req.verify = False
        
        try:
            backup_url = self.fortigate.mount_api_url()    # Mount the backup URL

            response = req.get(backup_url)    # Request backup via HTTP
            response.raise_for_status()    # Raise exception if status code is not successful

            with open(backup_path, 'wb') as f:
                f.write(response.content)

        except requests.RequestException as e:
            raise BackupFailedError(f'Backup job failed due to HTTP error: {e}')

        except FortigateOfflineError as e:
            raise BackupFailedError(f'Backup job failed, Fortigate is not connected: {e}')

        except Exception as e:
            raise BackupFailedError(f'Backup job failed: {e}')

    def schedule_backup(self, frequency):
        """Schedule automatic backups based on the specified frequency."""
        # TODO: This might be not necessary as argparse and cron jobs can do the same thing,
        # although this can be a way to define it more user-friendly
        pass

    def restore_from_backup(self, backup_file):
        """Restore configuration from a backup file."""
        # TODO: Check if this is possible and worth it
        pass
