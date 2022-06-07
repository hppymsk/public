#!/usr/bin/env python3

import warnings
from ldap3 import ALL
from ldap3 import Connection
from ldap3 import Server
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

'''Function for checking credentials against ldap. This can take a port value but have not
implemented that yet. A future to be done feature. Took ideas to implement from ldapdomaindump'''
def ldap_conn(params):

    auth = params.get("authentication")
    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    server = Server(host, get_info=ALL)
    count = params.get("count")
    domain = params.get("ldapdomain")
    username = domain + '\\' + username
    place = params.get("place")
    filelogger = params.get("filelogger")
            
    try:

        # print the host , username and password being checked
        print (f"ACCOUNT CHECK: [LDAP] Host: {host} Domain: {domain} User: {username} [{place} of {count}, {place} completed] Password: {password}")

        connection =  Connection(server, username, password,authentication=auth)#create connection
        if connection.bind():
            print (f"ACCOUNT FOUND: [LDAP] Host: {host} Domain: {domain} User: {username} Password: {password} [SUCCESS]")
            if filelogger != None:
                filelogger.debug(f"ACCOUNT FOUND: [LDAP] Host: {host} Domain: {domain} User: {username} Password: {password} [SUCCESS]")
    
    except:
        print(connection.result)
