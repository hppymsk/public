import json

with open('rewards.json', 'r') as read_file:
        rewards = json.load(read_file)
with open('2v2.json', errors='ignore') as read_file:
        twos = json.load(read_file)
with open('3v3.json', errors='ignore') as read_file:
        threes = json.load(read_file)
with open('5v5.json', errors='ignore') as read_file:
        fives = json.load(read_file)

def cutoff(bracket):

    if bracket in ['2', '2v2', '2s']:
        rank1 = 'Infernal Gladiator: ' + str(rewards['rewards'][0]['rating_cutoff']) + '\n'
        gladiator = 'Gladiator: ' + str(rewards['rewards'][0]['rating_cutoff']) + '\n'
        duelist = 'Duelist: ' + str(rewards['rewards'][0]['rating_cutoff']) + '\n'
        rival = 'Rival: ' + str(rewards['rewards'][0]['rating_cutoff']) + '\n'
        challenger = 'Challenger: ' + str(rewards['rewards'][0]['rating_cutoff'])
        cutoffs  = rank1 + gladiator + duelist + rival + challenger

    return cutoffs

'''for i in range(0,5):
    print(str(rewards['rewards'][i]['achievement']['name']) + ' - ' + str(rewards['rewards'][i]['rating_cutoff']))

top = ''
for i in range(0,10):
    top += '\n' + str(i+1) + ' - ' + str(threes['entries'][i]['team']['name']) + ' : ' + str(threes['entries'][i]['rating'])
print('Top 10 3v3 Teams:' + top)
'''
player = 'Vices'
twosteam = 'No 2v2 Team Found for ' + player
threesteam = 'No 3v3 Team Found for ' + player
fivesteam = 'No 5v5 Team Found for ' + player
'''
for x in range(len(twos['entries'])):
    if 'members' not in twos['entries'][x]['team']:
        continue
    for y in range(len(twos['entries'][x]['team']['members'])):
        if twos['entries'][x]['team']['members'][y]['character']['name'] == player:
           twosteam = str(twos['entries'][x]['team']['name']) + ' - ' + str(twos['entries'][x]['rating'])

for x in range(len(threes['entries'])):
    if 'members' not in twos['entries'][x]['team']:
        continue
    for y in range(len(threes['entries'][x]['team']['members'])):
       if threes['entries'][x]['team']['members'][y]['character']['name'] == player:
           threesteam = str(threes['entries'][x]['team']['name']) + ' - ' + str(threes['entries'][x]['rating'])

for x in range(len(fives['entries'])):
    if 'members' not in twos['entries'][x]['team']:
        continue
    for y in range(len(fives['entries'][x]['team']['members'])):
       if fives['entries'][x]['team']['members'][y]['character']['name'] == player:
           fivesteam = str(fives['entries'][x]['team']['name']) + ' - ' + str(fives['entries'][x]['rating'])

print(twosteam + '\n' + threesteam + '\n' + fivesteam)

for x in range(len(twos['entries'])):
    if 'members' not in twos['entries'][x]['team']:
        continue
    for y in range(len(twos['entries'][x]['team']['members'])):
        if twos['entries'][x]['team']['members'][y]['character']['name'] == player:
           twosteam = 'Personal: ' + str(twos['entries'][x]['team']['members'][y]['rating']) + ' | ' + 'Team: ' + str(twos['entries'][x]['rating'])

print(twosteam)
'''
msg = '!roll 1 100'
roll = msg.split('!roll ',1)[1]
print(roll[0])
