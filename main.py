''' Possible features to add
Handle special characters entered in names by user so script won't attempt to make invalid filenames

If LastYearMatches.txt doesn't exist, create it, prompt user to edit it, tell them they can paste from a spreadsheet, & use tab delimited file

Continue asking for player list if duplicates are found or there is an insufficient number of players

Keep any 2 players from being each other's givers & receivers.
E.g., keep Groot from buying for Tragdor when Tragdor is buying for Groot
Requires 5 players minimum?
'''

import os, random, sys, datetime

def PopulateGiversDictionary(givers, validatedPlayerList):
	for player in validatedPlayerList:
			givers[player] = []


def CheckGiverLengths(givers):
	activeGiver = ''
	for giver, receivers in givers.items():
		if len(receivers) < 2:
			activeGiver = giver
	return activeGiver


def AssignInitialReceivers(giver, givers, validatedPlayerList, lastMatches):
	# Assign full list of players to each giver
	for player in validatedPlayerList:
		givers[giver].append(player)

	# Remove giver from their own receiver list
	givers[giver].remove(giver)
	# Remove last year's receiver
	if giver in lastMatches:
		if lastMatches[giver] in givers[giver]:
			givers[giver].remove(lastMatches[giver])


def ChooseReceiver(activeGiver, givers, giversWithFinalReceivers):
	if len(givers[activeGiver]) > 0:
		activeReceiver = random.choice(givers[activeGiver])
	# Add giver & receiver pair to giversWithFinalReceivers{} then delete giver from givers{}
	giversWithFinalReceivers[activeGiver] = activeReceiver
	del givers[activeGiver]
	# Remove assigned receiver from all other giver's receivers lists
	for giver, receiverList in givers.items():
		if activeReceiver in receiverList:
			receiverList.remove(activeReceiver)


def Restart(givers, validatedPlayerList, lastMatches):
	PopulateGiversDictionary(givers, validatedPlayerList)
	for giver in givers:
		AssignInitialReceivers(giver, givers, validatedPlayerList, lastMatches)





def main():
	version = "0.0.3"
	givers = {}
	lastMatches = {}
	giversWithFinalReceivers = {}

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


	''' Test givers to enter in prompt:
	Trogdor, Satoshi Nakamoto, Aragorn, Nacho Libre, Li'l Sebastian, Groot, Brave Sir Robin
	'''
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
				# Remove non-alphanumeric chars from name
				# so it can be used in file naming
				alNumName = ''
				for char in player:
					if char.isalnum():
						alNumName += char
				# Keeps improperly entered names that are
				# only non-alphanumeric from being added
				# to validatedPlayerList as empty strings
				if len(alNumName) < 1:
					input(f'Invalid player name: {player}. Only contains special characters')
				else:
					validatedPlayerList.append(alNumName)
	totalPlayers = len(validatedPlayerList)
	if totalPlayers < 4:
		input(f'A minimum of 4 players is required, & you entered {totalPlayers}. Please type "Enter" to exit then re-run script')
		sys.exit()



	## SCRIPT BODY ##
	PopulateGiversDictionary(givers, validatedPlayerList)


	# Add all giver names to each giver then remove their own name & their last year receiver
	for giver in givers:
		AssignInitialReceivers(giver, givers, validatedPlayerList, lastMatches)


	# Choose final receivers
	while True:
		# If any giver has less than 3 receivers, they're set as the active giver. Otherwise, activeGiver returns as ''
		activeGiver = CheckGiverLengths(givers)
		if activeGiver == '':
			activeGiver = random.choice(list(givers.keys()))
		# The last giver will occasionally not have any receiver
		# options left due to the randomized choosing of
		# givers and receivers.
		# When this happens, the assignment process restarts
		try:
			ChooseReceiver(activeGiver, givers, giversWithFinalReceivers)
		except:
			Restart(givers, validatedPlayerList, lastMatches)
		# Check length of givers{} to see if all have been assigned receivers
		if len(givers.keys()) == 0:
			break


	# Update LastYearMatches.txt with this year's matches in
	# preparation for next year
	with open('LastYearMatches.txt', 'w') as file:
		print('# IMPORTANT. If you edit this file, you must follow the following syntax: <giver name>:<receiver name>\n', file=file)
		for giver, receiver in giversWithFinalReceivers.items():
			print(f'{giver}:{receiver}', file=file)


	# Creates one file per giver. Each file is named after a giver & contains their receiver's name
	matchesDir = 'Matches-' + datetime.datetime.today().strftime("%Y-%b-%d")
	# If a "Matches-<YYYYMMMDD>" dir exists, create another one
	# ending with "_<i>". The value of i depends on what
	# additional "_<i>" files already exist
	if os.path.exists(matchesDir):
		i = 2
		while True:
			dupMatchesDir = matchesDir + '_' + str(i)
			if os.path.exists(dupMatchesDir):
				i += 1
			else:
				os.mkdir(dupMatchesDir)
				matchesDir = dupMatchesDir
				break
	else:
		os.mkdir(matchesDir)
		
	for giver, receiver in giversWithFinalReceivers.items():
		with open(f'{matchesDir}\\{giver}.txt', 'w') as file:
			print(f'You are buying for {receiver}', file=file)

	print('\nFinished!')



# Run main() if file is being run rather than imported as a module
if __name__ == '__main__':
	main()
