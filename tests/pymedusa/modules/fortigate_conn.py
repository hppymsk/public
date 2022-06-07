#!/usr/bin/env python3

# Import all the libraries for the different prtocols
import requests
import warnings
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

def fortigate_conn(params):

    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    port = params.get("port")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    origin = 'https://' + host
    fortiurl = "https://{}:{}/remote/login?lang=en".format(host, port)
    loginurl = "https://{}:{}/remote/logincheck".format(host, port)

    headers = {
        'Host': host,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-store, no-cache, must-revalidate',
        'If-Modified-Since': 'Sat, 1 Jan 2000 00:00:00 GMT',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Content-Length': '52',
        'Origin': origin,
        'Connection': 'close',
        'Referer': fortiurl
    }

    data = "ajax=1&username={}&realm=&credential={}".format(username,password)

    try:

        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [FORTIGATE] Target: {host} Port: {port} User: {username} [{place} of {count}, {place} completed] Password: {password}")
        print(f"Login URL: {loginurl}")
        query = requests.post(loginurl,data=data,headers=headers, verify=False, allow_redirects=True)
        if query.status_code == 200:
            if 'SVPNTMPCOOKIE' in query.headers['Set-Cookie']:
                print(f"ACCOUNT FOUND: [FORTIGATE] Target: {host} Port: {port} User: {username} Password: {password} [SUCCESS]")
                if filelogger != None:
                    filelogger.debug(f"ACCOUNT FOUND: [FORTIGATE] Target: {host} Port: {port} User: {username} Password: {password} [SUCCESS]")
    except:
        pass   
