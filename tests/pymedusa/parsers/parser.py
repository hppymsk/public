#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError
from ipaddress import ip_network
from itertools import product
from modules.basic_conn import basic_conn
from modules.cisco_conn import cisco_conn
from modules.citrix_conn import citrix_conn
from modules.ews_conn import ews_conn
from modules.fortigate_conn import fortigate_conn
from modules.ftp_conn import ftp_conn
from modules.gp_conn import gp_conn
from modules.jump_conn import jump_conn, get_tokens
from modules.ldap_conn import ldap_conn
from modules.o365_conn import o365_conn
from modules.okta_conn import okta_conn
from modules.owa_conn import owa_conn
from modules.smb_conn import smb_conn
from modules.ssh_conn import ssh_conn
from modules.me_conn import me_conn
from modules.adfs_conn import adfs_conn, calculate_values
from modules.rdweb_conn import rdweb_conn, rdweb_params
from os.path import isfile
import logging

class Parser:
	"""Class to accept the username, userfile, password and password file 
	arguments and parse them out to be made available to any protocol"""


	def parse_values (self,arg_dict):
		#print(arg_dict)
		return_dict = {}

		if isfile(arg_dict.get("username")):
			with open (arg_dict.get("username","r")) as f:
				userfile_content = f.read().splitlines()
				f.close()
			return_dict['username'] = userfile_content
		elif isinstance(arg_dict.get("username"), str):
			return_dict['username'] = arg_dict.get("username")
		else:
			print ("Username/Username File not found!")

		if arg_dict.get("password") != None:
			if isfile(arg_dict.get("password")):
				with open (arg_dict.get("password","r")) as f:
					passfile_content = f.read().splitlines()
					f.close()	
				return_dict["password_type"] = "plaintext"	
				return_dict['password'] = passfile_content
			elif isinstance(arg_dict.get("password"), str):	
				return_dict['password'] = arg_dict.get("password")
				return_dict["password_type"] = "plaintext"	
			else:
				print ("Password/Password File not found!")
		
		if (arg_dict.get('host')):
			if isfile(arg_dict.get("host")):
				with open (arg_dict.get("host","r")) as f:
					hostfile_content = f.read().splitlines()
					f.close()
				return_dict['host'] = hostfile_content
			elif isinstance(arg_dict.get("host"), str):	
				return_dict['host'] = arg_dict.get("host")		
			else:
				print ("Host/Host File not found!")

		if (arg_dict.get('cidr')):
			interim = ip_network(arg_dict.get('cidr'))
			subnet = []
			for ips in interim.hosts():
				subnet.append(str(ips))
			return_dict['host'] = subnet
		

		if (arg_dict.get('hash')):
			if isfile(arg_dict.get("hash")):
				with open (arg_dict.get("hash","r")) as f:
					hash_content = f.read().splitlines()
					f.close()
				return_dict['password'] = hash_content
				return_dict['password_type'] = 'hash'
			elif isinstance(arg_dict.get("hash"), str):	
				return_dict['password'] = arg_dict.get("hash")
				return_dict['password_type'] = 'hash'
			else:
				print ("Hash/Hash File not found!")
			
		if arg_dict.get("extra"):
			if arg_dict.get("extra") == 'S' or arg_dict.get("extra") == 's' :
				return_dict['password_type'] = 'plaintext'
			# else:
			# 	return_dict['password_type'] = 'hash'

		if arg_dict.get("output"):
			logger = logging.getLogger('pymedusa')
			logger.setLevel(logging.DEBUG)

			# Output response to a File
			filename = logging.FileHandler(arg_dict.get("output"))
			filename.setLevel(logging.DEBUG)
			logger.addHandler(filename)

			# Output response to Screen
			# screenOutput = logging.StreamHandler(sys.stdout)
			# screenOutput.setLevel(logging.DEBUG)
			# logger.addHandler(screenOutput)

			return_dict['filelogger'] = logger

		for key, value in arg_dict.items():
			if key not in ['username','password','hash','host','cidr']:
				if value != None:
					return_dict[key] = arg_dict.get(key)			
		return return_dict


	'''This function passes the arguments for password spraying to the specified
	module for the rest of the heavy lifting'''
	def workerfunc(self,params):

		function = {
			'basic':basic_conn,
			'cisco': cisco_conn,
			'citrix':citrix_conn,
			'ews':ews_conn,
			'fortigate':fortigate_conn,
			'ftp':ftp_conn,
			'globalprotect':gp_conn,
			'jumpcloud':jump_conn,
			'ldap':ldap_conn,
			'o365':o365_conn,
			'okta':okta_conn,
			'owa':owa_conn,
			'smb': smb_conn,
			'ssh':ssh_conn,
			'manageengine':me_conn,
			'adfs':adfs_conn,
			'rdweb':rdweb_conn
		}

		host_urls = {
			#'o365':'https://autodiscover-s.outlook.com/autodiscover/autodiscover.xml',
			'o365':'https://login.microsoft.com',
			'jumpcloud':'https://console.jumpcloud.com/userconsole/auth'
		}

		# Here is where we convert the main three (host, username and password) from files to a list
		if isinstance(params.get("password"), (str)):
			password = ''.join(params.get("password"))
			if len(password.split()) > 1:
				password = password.splitlines()
			else:
				password = password.split(' ')			
		else:
			password = params.get("password")

		if isinstance(params.get("username"), (str)):
			username = ''.join(params.get("username"))
			username = username.split(' ')
		else:
			username = params.get("username")

		if params.get('host'):
			if isinstance(params.get("host"), (str)): #Checks if a single host is passed
				host = ''.join(params.get("host")) #Changes to a list
				host = host.split(' ') #Make into a string
			else:
				host= params.get("host") #Pass it back as a list
		elif params.get('modules') == 'citrix': #I do not know why I did this!
			host = params.get('host')
			host = ''.join(list(host))
			host = host.split(' ')
		elif params.get('modules') == 'o365':
			if params.get('url') != None:
				host = params.get('url')
				host = ''.join(list(host))
				host = host.split(' ')
			else:
				host = host_urls[params.get('modules')]
				host = ''.join(list(host))
				host = host.split(' ')
		else:
			host = host_urls[params.get('modules')]
			host = ''.join(list(host))
			host = host.split(' ')

		# if params.get('extra'):
		# 	if params.get("extra") == 'N' or params.get("extra") == 'n':
		# 		password = '31d6cfe0d16ae931b73c59d7e0c089c0'

		results = []
		count = len(username)
		place = 0
		value = []
		if params.get('extra'):
			if params.get('extra')  == 'S' or params.get('extra') == 's':
				value = product(host,username)
		else:
			value = product (host,password,username)
		conn_args = {}

		# get xsrf tokens for jumpcloud module
		if params.get('modules') == 'jumpcloud':
			conn_args['xsrf'], conn_args['xsrftoken'] = get_tokens()

		# get dafs tokens for adfs module
		if params.get('modules') == 'adfs':
			conn_args['dafs_url'] = calculate_values(params.get('host'))

		if params.get('modules') == 'rdweb':
			conn_args['rdp_vars'] = rdweb_params(params.get('host'))

		# Put all other values in conn_args dictionary
		for key, values in params.items():
			if key not in ['host','username','password']:
				if values != 'None':
					conn_args[key]=params.get(key)

		for s in value:
			conn_args["host"] = s[0]
			if params.get('extra'):
				if params.get('extra')  == 'S' or params.get('extra') == 's':
					conn_args["password"] = s[1]
					conn_args["username"] = s[1]
			else:
				conn_args["password"] = s[1]
				conn_args["username"] = s[2]
			conn_args["count"] = count
			conn_args["place"] = place + 1
			conn_args["password_type"] = params.get("password_type")
			place = place + 1

			try:
				# Starting the password spraying with multiple threads (hopefully) need more investigation
				with ThreadPoolExecutor(max_workers=params.get('thread')) as executor:
					future = executor.submit(function[params.get('modules')], conn_args)
					results.append(future.result(timeout=params.get('conntimeout')))
			except TimeoutError:
				if params.get('extra'):
					print (f"Timeout reached for {s[1]}. Aborting.")
				else:
					print (f"Timeout reached for {s[2]}. Aborting.")

		#return results
