#!/usr/bin/env python3

# Import all the libraries for the different prtocols
import warnings
from impacket.smbconnection import SMBConnection
from impacket.smbconnection import SessionError
from socket import error as socket_error
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
	filelogger = params.get("filelogger")
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

		try:	
			connection_name.logoff()
		except:
			pass

		connection = SMBConnection(server,server)
        #print the host , username and password being checked
		print (f"ACCOUNT CHECK: [SMB] Host: {server} Domain: {domain} User: {username} [{place} of {count}, {place} completed] Password: {password}")

		if ptype == "plaintext":
			login_true = connection.login(username,password,domain) #check if login works
		else:
			lmhash = 'aad3b435b51404eeaad3b435b51404ee'
			login_true = connection.login(username,'',domain,lmhash,password)
		admin_check = connection.connectTree('ADMIN$') #check if admin access is possible
				
		#check if login works and if admin access is possible and print out results
		if (login_true == True and admin_check == 1):
			print (f"ACCOUNT FOUND: [SMB] Host: {server} Domain: {domain} User: {username} Password: {password} [SUCCESS - (Admin$ Access Allowed)]")
			if filelogger != None:
				filelogger.debug(f"ACCOUNT FOUND: [SMB] Host: {server} Domain: {domain} User: {username} Password: {password} [SUCCESS - (Admin$ Access Allowed)]")

		connection.logoff()

	#Check what the Error is 
	except socket_error as msg:
		print("Error: {}".format(msg))
	except SessionError as e:
		if 'STATUS_LOGON_FAILURE' in e.getErrorString():
			pass

		elif "STATUS_ACCESS_DENIED" in e.getErrorString():
			
			if login_true == True:
				print (f"ACCOUNT FOUND: [SMB] Host: {server} Domain: {domain} User: {username} Password: {password} [SUCCESS - ({e.getErrorString()[0]})]")
				if filelogger != None:
					filelogger.debug(f"ACCOUNT FOUND: [SMB] Host: {server} Domain: {domain} User: {username} Password: {password} [SUCCESS - ({e.getErrorString()[0]})]")

		elif "STATUS_ACCOUNT_LOCKED_OUT" in e.getErrorString():
			print (f"ACCOUNT LOCKED: [SMB] Host: {server} Domain: {domain} User: {username} Password: {password} [LOCKED- ({e.getErrorString()[0]})]")
			if filelogger != None:
				filelogger.debug(f"ACCOUNT LOCKED: [SMB] Host: {server} Domain: {domain} User: {username} Password: {password} [LOCKED - ({e.getErrorString()[0]})]")

		else:
			print (f"ACCOUNT FOUND: [SMB] Host: {server} Domain: {domain} User: {username} Password: {password} [SUCCESS - ({e.getErrorString()[0]})]")
			if filelogger != None:
				filelogger.debug(f"ACCOUNT FOUND: [SMB] Host: {server} Domain: {domain} User: {username} Password: {password} [SUCCESS - ({e.getErrorString()[0]})]")