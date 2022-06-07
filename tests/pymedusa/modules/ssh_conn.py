#!/usr/bin/env python3

# Import all the libraries for the different prtocols
import paramiko
import warnings
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)


'''Function to password guess against SSH.
Will need to move the client object outside the loop for faster execution'''
def ssh_conn(params):

    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    port = params.get("sshport")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:

        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [SSH] Target: {host} Port:{port} User: {username} [{place} of {count}, {place} completed] Password: {password}")
        client.connect(hostname=host, port=port, username=username, password=password, timeout=3)

    except paramiko.AuthenticationException:
        pass
    except paramiko.SSHException:
        print ("Anti-Brute measures triggered")
    else:
        try:
            print(f"ACCOUNT FOUND: [SSH] Target: {host} Port:{port} User: {username} Password: {password} [SUCCESS]")
            if filelogger != None:
                filelogger.debug(f"ACCOUNT FOUND: [SSH] Target: {host} Port:{port} User: {username} Password: {password} [SUCCESS]")
        except:
            pass
