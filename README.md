# PyFortiManagerLite
## Disclaimer
> ***This program is not affiliated with, endorsed, or sponsored by the official Fortinet FortiManager application. It does not derive from nor share features with the official Fortinet FortiManager application. It is not intended for use in an enterprise production environment, and it does not possess any licensing agreement with Fortinet. Use of this program is at your own risk, and the creators of this program hold no responsibility for any consequences resulting from its use.***
>
> ***This is a personal project that I am working on, which involves making API requests to a set of FortiGates. It is provided without warranty and is to be used at your own risk. I make no guarantees regarding the accuracy, reliability, or suitability of this software for any purpose. By using this software, you agree that I will not be liable for any damages or losses arising from its use. Please exercise caution and ensure compliance with all applicable laws and regulations.***

## Greetings
This app is mainly based in [mcarneir0 repo](https://github.com/mcarneir0/fortigate-backup-api) where I checked all the code and implement my solution according to my needs.

I would also like to thank my teammates who encouraged me to develop this project since my home lab is getting pretty big and multi_vdom enviroments tend to get messy when there's no Fabric Management.

Lastly, I would like to thank my job for bring all the idea to my head.

## Summary
- [Description](https://github.com/userS4B0/PyFortiManagerLite#Description)
- [Installation](https://github.com/userS4B0/PyFortiManagerLite#Installation)
- [Usage](https://github.com/userS4B0/PyFortiManagerLite#Usage)
- [Configuration](https://github.com/userS4B0/PyFortiManagerLite#Configuration)
  - [CSV file](https://github.com/userS4B0/PyFortiManagerLite#csv-file-format)
  - [SSL certificate](https://github.com/userS4B0/PyFortiManagerLite#ssl-certificate-warnings)
  - [Folders](https://github.com/userS4B0/PyFortiManagerLite#folder-structure)
- [Generating API key](https://github.com/userS4B0/PyFortiManagerLite#generating-the-api-key)
  1. [Access the firewall](https://github.com/userS4B0/PyFortiManagerLite#1-access-the-firewall)
  2. [Create REST API user](https://github.com/userS4B0/PyFortiManagerLite#3-create-a-new-rest-api-admin)
     - [Trusted hosts warning](https://github.com/userS4B0/PyFortiManagerLite#warning)
- [Environment](https://github.com/userS4B0/PyFortiManagerLite#environment)
- [References](https://github.com/userS4B0/PyFortiManagerLite#references)
- [License](https://github.com/userS4B0/PyFortiManagerLite#license)




## Description
This app makes it easy to perform backups of multiple Fortigate firewalls. It reads a list of Fortigates from a CSV file, performs a backup of each one, and saves the backup file to a local directory.

## Installation
#### Requirements
- [Python 3.6](https://www.python.org/downloads/) or newer
- [Requests](https://pypi.org/project/requests/) module

*Installation Coming Soon*

## Usage
Add the following details of each managed FortiGate device in the `/data/inventory.csv`:

- Name
- Managment IP 01
- Managment IP 02
- VDOM Type
- API Token ([Need one?]((https://github.com/userS4B0/PyFortiManagerLite#generating-the-api-key)))

Run the `main.py` file to perform a backup of all Fortigates without user input. Useful for use with cron job or scheduled tasks.
```bash
  python main.py
```

*ArgParse and CLI UI Functionality Coming Soon*

## Configuration
### CSV file format
The `inventory.csv` file should have the following format:

```csv
Name,Managment IP 01,Managment IP 02,VDOM Type,API Token
FortigateName1,134.23.12.12,,global,hereyoucanputyourtokenforapiuser
FortigateName2,12.0.0.12:3443,,global,hereyoucanputyourtokenforapiuser
FortigateName3,192.168.1.1:8081,,vdom&vdom=MyVDOMName,hereyoucanputyourtokenforapiuser
```
> There's an `inventory_example.csv` provided
> FQDN addresses can be used

Where:

- `Name`: A name to identify the FortiGate
- `Managment IP 01`: Primary IP address of the FortiGate
- `Managment IP 02`: Secondary IP address of the FortiGate (optional)
- `VDOM Type`:
- `API Token`: API key provided by the FortiGate

##### Notes:

1. If you are using a custom administrative port (other than 443) you should include with the IP address with `<IP>:<PORT>` format.
2. If your Fortigate does not have a secondary IP address, just leave it blank as `FortigateName1` example.

### SSL certificate warnings

By default, the script doesn't verify the SSL certificate of the FortiGates. **If you have an SSL signed certificate, you may want to enable this feature.** To do so, comment the following two lines at `/src/api_handlers.py`:

```python
requests.packages.urllib3.disable_warnings()
req.verify = False
```

### Folder structure

The script creates two folders:

- `backups`: Contains the backup files.
- `logs`: Contains the log files.

The backup files are saved in a subfolder on `backups` with the current date in the format yyyy-mm-dd.

The log files are saved in the `logs` folder with the name `pfgtmgrl_<current_date>.log`.

## Generating the API key

You need to create a _REST API Admin_ with _super_admin_ rights firstly. Follow the steps below.

> You can also generate the user via GUI but the *super_admin* profile to the api user is only avalible via CLI

### 1. Access the firewall via ssh
    
Login to the firewall throug ssh with your credentials and make sure you have _super_admin_ rights.

```bash
ssh -p <your_administrative_ssh_port> <your_admin_user>@<your_administrative_ip>
```

### 2. Create a new Rest API administrator

> *This coniguration via CLI was tested in a multi_vdom enviroment*, for more information about how to create a Rest API admin please check [Fortinet Oficial Documentation](https://docs.fortinet.com/document/fortigate/7.4.3/administration-guide/399023/rest-api-administrator)

```bash
config system api-user
  edit pfgtmgrl_user # Choose a name of your preference
    set comments "Rest API user for PyFGTManagerLite tool" # Optional
    set accprofile super_admin
    config trusthost
      edit 1
        set ipv4-trusthost <IP/NETMASK> # CIDR notation is allowed
        next
    end
  set vdom <VdomName1> <VdomName2> <VdomNameX> # Most likely you'll want to reach all your vdoms from this user
end
```

Now you'll have to acess the FortiGate GUI and go to `System > Administrators`

Then select your new Rest API admin and clock `generate API Token`

### WARNING!

> It is **highly recommended that you fill in your IP or network** in the _Trusted Hosts_ so that you guarantee that only requests made from these addresses will be accepted, **otherwise anyone with access to the API token will have unrestricted access to the firewall.**
> 
> Click OK and you will be prompted to store the generated API key in a secure location. Keep in mind that this key will not be shown again so if you lose it, you will have to generate another one.

## Environment

Tested with:

- Windows 11
- Python 3.11.2
- FortiOS 6.0.x / 6.2.x / 7.0.x / 7.2.x

## References

 - [FortiGate REST API Token Authentication](https://www.insoftservices.uk/fortigate-rest-api-token-authentication/)
 - [Technical Tip: Get backup config file on FortiGate using RestAPI via Python script](https://community.fortinet.com/t5/FortiGate/Technical-Tip-Get-backup-config-file-on-FortiGate-using-RestAPI/ta-p/202286)
 - [REST API administrator](https://docs.fortinet.com/document/fortigate/7.4.3/administration-guide/399023/rest-api-administrator)

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](https://github.com/userS4B0/PyFortiManagerLite/LICENSE.md) file for details.


