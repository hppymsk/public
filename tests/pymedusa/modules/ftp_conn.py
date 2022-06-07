#!/usr/bin/env python3

# Import all the libraries for the different prtocols
import requests
import warnings
from ftplib import FTP
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def ftp_conn(params):

    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    port = params.get('ftpport')
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")

    try:
        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [FTP] Target: {host} Port:{port} User: {username} [{place} of {count}, {place} completed] Password: {password}")
        server = FTP()
        server.connect(host, port)
        server.login(username, password)
        server.quit()
    except ftplib.error_perm:
        pass
    else:
        print(f"ACCOUNT FOUND: [FTP] Target: {host} Port:{port} User: {username} Password: {password} [SUCCESS]")
        filelogger.debug(f"ACCOUNT FOUND: [FTP] Target: {host} Port:{port} User: {username} Password: {password} [SUCCESS]")