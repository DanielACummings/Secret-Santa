''' Possible features to add
Handle special characters entered in names by user so script won't attempt to make invalid filenames

Make timestamped dir for each script run

Use "if __name__ == '__main__'" setup

Continue asking for player list if duplicates are found or there is an insufficient number of players

Keep any 2 players from being each other's givers & receivers.
E.g., keep Groot from buying for Tragdor when Tragdor is buying for Groot
'''

import os, random, sys

version = "0.0.2"

## GLOBAL VARIABLES ##
'''
List of test givers to enter in prompt:
Trogdor, Satoshi Nakamoto, Aragorn, Nacho Libre, Li'l Sebastian, Groot, Brave Sir Robin
'''

givers = {}
lastMatches = {}
giversWithFinalReceivers = {}


## FUNCTIONS ##
def PopulateGiversDictionary(validatedPlayerList):
	for player in validatedPlayerList:
			givers[player] = []


def CheckGiverLengths():
	activeGiver = ''
	for giver, receivers in givers.items():
		if len(receivers) < 2:
			activeGiver = giver
	return activeGiver


def AssignInitialReceivers(giver):
	# Assign full list of players to each giver
	for player in validatedPlayerList:
		givers[giver].append(player)

	# Remove giver from their own receiver list
	givers[giver].remove(giver)
	# Remove last year's receiver
	if giver in lastMatches:
		if lastMatches[giver] in givers[giver]:
			givers[giver].remove(lastMatches[giver])


def ChooseReceiver(activeGiver):
	if len(givers[activeGiver]) > 0:
		activeReceiver = random.choice(givers[activeGiver])
	# Add giver & receiver pair to giversWithFinalReceivers{} then delete giver from givers{}
	giversWithFinalReceivers[activeGiver] = activeReceiver
	del givers[activeGiver]
	# Remove assigned receiver from all other giver's receivers lists
	for giver, receiverList in givers.items():
		if activeReceiver in receiverList:
			receiverList.remove(activeReceiver)


def Restart():
	PopulateGiversDictionary(validatedPlayerList)
	for giver in givers:
		AssignInitialReceivers(giver)





## SETUP ##
print('Secret Santa Script version ' + version)

# Populate lastMatches from LastYearMatches.txt
with open('LastYearMatches.txt') as file:
	lines = file.readlines()
	for line in lines:
		if not line.startswith('#') and not line.strip() == (''):
			oldMatch = line.strip().split(':')
			giver = oldMatch[0]
			receiver = oldMatch[1]
			lastMatches[giver] = receiver


# Get & validate player list
playerList = input('Enter list of people participating separated by commas: ').split(',')
validatedPlayerList = []
# Add players from playerList to validatedPlayerList that aren't empty strings or duplicates
for player in playerList:
	player = player.strip()
	if player in validatedPlayerList:
		input(f'Duplicate player found: {player}. Please type "Enter" to exit then re-run script')
		sys.exit()
	else:
		if player != '':
			validatedPlayerList.append(player)
totalPlayers = len(validatedPlayerList)
if totalPlayers < 4:
	input(f'A minimum of 4 players is required, & you entered {totalPlayers}. Please type "Enter" to exit then re-run script')
	sys.exit()


PopulateGiversDictionary(validatedPlayerList)


# Add all giver names to each giver then remove their own name & their last year receiver
for giver in givers:
	AssignInitialReceivers(giver)



## CHOOSE FINAL RECEIVERS ##
while True:
	# If any giver has less than 3 receivers, they're set as the active giver. Otherwise, activeGiver returns as ''
	activeGiver = CheckGiverLengths()
	if activeGiver == '':
		activeGiver = random.choice(list(givers.keys()))
	# The last giver will occasionally not have any receiver
	# options left due to the randomized choosing of
	# givers and receivers.
	# When this happens, the assignment process restarts
	try:
		ChooseReceiver(activeGiver)
	except:
		Restart()
	# Check length of givers{} to see if all have been assigned receivers
	if len(givers.keys()) == 0:
		break



## CREATE & EDIT FILES ##
# Updates LastYearMatches.txt with this year's matches in
# preparation for next year
with open('LastYearMatches.txt', 'w') as file:
	 print('# IMPORTANT. If you edit this file, you must follow the following syntax: <giver name>:<receiver name>\n', file=file)
	 for giver, receiver in giversWithFinalReceivers.items():
		 print(f'{giver}:{receiver}', file=file)


# Creates one file per giver. Each file is named after a giver & contains their receiver's name
cwd = os.getcwd()
matchesDir = cwd + '\\SecretSantaMatches'
# Make dir to put giver files into if it doesn't exist
if not os.path.exists(matchesDir):
	os.mkdir(matchesDir)
for giver, receiver in giversWithFinalReceivers.items():
	 with open(f'{matchesDir}\\{giver}.txt', 'w') as file:
		 print(f'You are buying for {receiver}', file=file)
