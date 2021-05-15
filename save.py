import json
'''
data = {}  
data['people'] = []  
data['people'].append({'name': 'Scott', 'website': 'stackabuse.com', 'from': 'Nebraska'})
data['people'].append({'name': 'Larry', 'website': 'google.com', 'from': 'Michigan'})
data['people'].append({'name': 'Tim', 'website': 'apple.com', 'from': 'Alabama'})


data = {1: {'name': 'Scott', 'wins': '1'},
		2: {'name': 'Larry', 'wins': '2'},
		3: {'name': 'Tim', 'wins': '3'}}
y = 1
x = 'name'
print(data[y][x] + data[y]['wins'])


with open('data.txt', 'w') as outfile:  
    json.dump(data, outfile, indent=4)
'''
def highScores():
	with open('data.txt') as json_file:  
	    data = json.load(json_file)

	    for p in data:
	        print(data[p]['name'] + ': ' + data[p]['wins'])
	        print('')
	        top_score = 0
	        top_score = ''
	        if data[p]['wins'] > top_score:
	        	top_score = data[p]['wins']
	        	top_scores = data[p]['name']
	    print('Luckiest Player: ' + top_scores + ' with ' + top_score + ' wins.')

def updateScores(discID):
	with open('data.txt') as json_file:
		data = json.load(json_file)
		for p in data:
			if discID in data[p].values():
				#Occurs when existing player wins

				newInt = (int(data[p]['wins']) + 1)
				
				data[p]['wins'] = str(newInt)
				print(discID + ' now has ' + str(newInt) + ' wins.')
				
				with open('data.txt', 'w') as outfile:
					json.dump(data, outfile, indent=4)
				
				return

		#Occurs when new player wins
		x = int(p) + 1
		data[x] = {'name': discID, 'wins': '1'}
		#Write new player data to file
		with open('data.txt', 'w') as outfile:
			json.dump(data, outfile, indent=4)

updateScores('Tim')
highScores()