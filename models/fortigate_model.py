import requests

class FortigateOfflineError(Exception):
    """
    Custom exception for indicating that the FortiGate device is offline.
    
    This exception is raised when the FortiGate device cannot be reached or is offline.
    """
    pass

class FortiGate:
    def __init__(self, name: str, mgmt_ip_01: str, mgmt_ip_02: str, vdom_type: str, s_signed_cert: bool, api_token: str):
        """
        Initializes a FortiGate instance.
        
        Args:
            name (str): The name of the FortiGate device.
            mgmt_ip_01 (str): The first management IP address of the device.
            mgmt_ip_02 (str): The second management IP address of the device.
            vdom_type (str): The VDOM type of the device.
            s_signed_cert (bool): Whether a self-signed certificate is used.
            api_token (str): The API token for accessing the device.
        """
        self.name = name
        self.mgmt_ips = [mgmt_ip_01, mgmt_ip_02]
        self.vdom_type = vdom_type
        self.s_signed_cert = s_signed_cert
        self.api_token = api_token
        
        self.access_ip = None

    def get_access_ip(self):
        """
        Tries to determine the access IP address by testing both management IPs.
        
        Returns:
            str: The access IP address.
        
        Raises:
            FortigateOfflineError: If both management IPs are offline.
        """
        for ip in self.mgmt_ips:
            try:
                self.test_connectivity(ip)
                self.access_ip = ip
                return self.access_ip
            except FortigateOfflineError:
                pass
        
        raise FortigateOfflineError("No matching mgmt ip to access the device")

    def test_connectivity(self, ip):
        """
        Tests the connectivity with a given IP address.
        
        Args:
            ip (str): The IP address to test connectivity with.
        
        Raises:
            FortigateOfflineError: If the device is offline.
        """
        req = requests.session()
        
        if self.s_signed_cert:
            requests.packages.urllib3.disable_warnings()
            req.verify = False
            
        try:
            # Attempt to send a request to the FortiGate with a timeout of 3 seconds
            req.get(f'https://{ip}', timeout=3)
        except Exception:
            raise FortigateOfflineError(f'FortiGate is offline at {ip}')

    def mount_api_url(self):
        """
        Mounts the API URL using the access IP address and the API token.
        
        Returns:
            str: The API URL.
        
        Raises:
            FortigateOfflineError: If no access IP is provided.
        """
        # Define the URI for the API endpoint
        URI = f'/api/v2/monitor/system/config/backup?scope={self.vdom_type}&access_token='
        
        # Obtain the access IP address
        access_ip = self.get_access_ip()
        
        # If access IP is obtained, construct the API URL
        if access_ip:
            return f'https://{access_ip}{URI}{self.api_token}'
        else:
            raise FortigateOfflineError("No access IP provided")
