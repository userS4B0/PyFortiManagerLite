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
        self.mgmt_ip_01 = mgmt_ip_01
        self.mgmt_ip_02 = mgmt_ip_02
        self.vdom_type = vdom_type
        self.s_signed_cert = s_signed_cert
        self.api_token = api_token
        
        self.access_ip = None

    # Getter methods for instance attributes
    def get_name(self): return self.name
    def get_management_ip_01(self): return self.mgmt_ip_01
    def get_management_ip_02(self): return self.mgmt_ip_02
    def get_vdom_type(self): return self.vdom_type
    def has_self_signed_certificate(self): return self.s_signed_cert
    def get_api_token(self): return self.api_token
    
    def get_access_ip(self):
        """
        Tries to determine the access IP address by testing both management IPs.
        
        Returns:
            str: The access IP address.
        
        Raises:
            FortigateOfflineError: If both management IPs are offline.
        """
        # Try to connect using the first management IP
        try:
            self.connectivity_test(self.mgmt_ip_01)
            self.access_ip = self.mgmt_ip_01
            return self.access_ip
        except FortigateOfflineError:
            pass

        # If the first management IP fails, try the second one
        try:
            self.connectivity_test(self.mgmt_ip_02)
            self.access_ip = self.mgmt_ip_02
            return self.access_ip
        except FortigateOfflineError:
            pass

        # If both management IPs fail, raise an error
        raise FortigateOfflineError("No matching mgmt ip to access the device")

    def connectivity_test(self, ip):
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
        except:
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
