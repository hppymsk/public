import requests
import json
import urllib3
import os

urllib3.disable_warnings()
token_url = "https://us.battle.net/oauth/token"

twos_api_url = "https://us.api.blizzard.com/data/wow/pvp-season/1/pvp-leaderboard/2v2?namespace=dynamic-classic-us&locale=en_US"
threes_api_url = "https://us.api.blizzard.com/data/wow/pvp-season/1/pvp-leaderboard/3v3?namespace=dynamic-classic-us&locale=en_US"
fives_api_url = "https://us.api.blizzard.com/data/wow/pvp-season/1/pvp-leaderboard/5v5?namespace=dynamic-classic-us&locale=en_US"
rewards_api_url = "https://us.api.blizzard.com/data/wow/pvp-season/1/pvp-reward/index?namespace=dynamic-classic-us&locale=en_US"

#client (application) credentials
client_id = os.environ['BLIZZ-CLIENT-ID']
client_secret = os.environ['BLIZZ-CLIENT-SECRET']

#step A, B - single call with client credentials as the basic auth header - will return access_token
data = {'grant_type': 'client_credentials'}

access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

tokens = json.loads(access_token_response.text)

print ("access token: " + tokens['access_token'])

#step B - with the returned access_token we can make as many calls as we want

api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}

#2v2 File
api_call_response = requests.get(twos_api_url, headers=api_call_headers, verify=False)
print('Writing 2v2 file')
with open('2v2.json', 'w') as f:
    f.write(api_call_response.text)

#3v3 File
api_call_response = requests.get(threes_api_url, headers=api_call_headers, verify=False)
print('Writing 3v3 file')
with open('3v3.json', 'w') as f:
    f.write(api_call_response.text)

#5v5 Files
api_call_response = requests.get(fives_api_url, headers=api_call_headers, verify=False)
print('Writing 5v5 file')
with open('5v5.json', 'w') as f:
    f.write(api_call_response.text)

#Rewards File
api_call_response = requests.get(rewards_api_url, headers=api_call_headers, verify=False)
print('Writing Rewards file')
with open('rewards.json', 'w') as f:
    f.write(api_call_response.text)

