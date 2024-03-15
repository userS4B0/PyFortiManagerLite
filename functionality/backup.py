import requests

from api.fortigate import FortiGate, FortigateOfflineError

class BackupFailedError(Exception):
    """Custom exception for indicating that the Backup Job Failed"""
    pass

class Backup:
    def __init__(self, fortigate: FortiGate):
        self.fortigate = fortigate

    def perform_backup(self, backup_path):
        try:
            backup_url = self.fortigate.mount_api_url()    # Mount the backup URL

            response = requests.get(backup_url)    # Request backup via HTTP
            response.raise_for_status()    # Throws Exception if status code is not successful

            with open(backup_path, 'wb') as f:
                f.write(response.content)

        except requests.RequestException as e:
            raise BackupFailedError(f'Backup job failed due to HTTP error: {e}')

        except FortigateOfflineError as e:
            raise BackupFailedError(f'Backup job failed, Fortigate is not connected: {e}')

        except Exception as e:
            raise BackupFailedError(f'Backup job failed: {e}')

    def schedule_backup(self, frequency):
        # TODO: This might be not neccessary cause aurgparse and cron jobs can do the same thing, although this can be a way to define it more user frendly
        pass

    def restore_from_backup(self, backup_file):
        # TODO: Check if this is possible and worthit
        pass