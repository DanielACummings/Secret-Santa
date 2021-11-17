''' Possible features to add
Make error handling function

If LastYearMatches.txt doesn't exist, create it, prompt user to edit it, tell them they can paste from a spreadsheet, & use tab delimited file

Continue asking for player list if duplicates are found or there is an insufficient number of players

Keep any 2 players from being each other's givers & receivers.
E.g., keep Groot from buying for Tragdor when Tragdor is buying for Groot
Requires 5 players minimum?
'''

import os, random, sys, datetime

def PopulateGiversDictionary(givers: dict, validatedPlayers: list) -> None:
	for player in validatedPlayers:
			givers[player] = []


def CheckGiverLengths(givers: dict) -> str:
	activeGiver = ''
	for giver, receivers in givers.items():
		if len(receivers) < 2:
			activeGiver = giver
	return activeGiver


def AssignInitialReceivers(giver: str, givers: dict, validatedPlayers: list, lastMatches: dict) -> None:
	# Assign full list of players to each giver
	for player in validatedPlayers:
		givers[giver].append(player)

	# Remove giver from their own receiver list
	givers[giver].remove(giver)
	# Remove last year's receiver
	if giver in lastMatches:
		if lastMatches[giver] in givers[giver]:
			givers[giver].remove(lastMatches[giver])


def ChooseReceiver(activeGiver: str, givers: dict, giversWithFinalReceivers: dict) -> None:
	if len(givers[activeGiver]) > 0:
		activeReceiver = random.choice(givers[activeGiver])
	# Add giver & receiver pair to giversWithFinalReceivers{} then delete giver from givers{}
	giversWithFinalReceivers[activeGiver] = activeReceiver
	del givers[activeGiver]
	# Remove assigned receiver from all other giver's receivers lists
	for giver, receiverList in givers.items():
		if activeReceiver in receiverList:
			receiverList.remove(activeReceiver)
5

def Restart(givers: dict, validatedPlayers: list, lastMatches: dict) -> None:
	PopulateGiversDictionary(givers, validatedPlayers)
	for giver in givers:
		AssignInitialReceivers(giver, givers, validatedPlayers, lastMatches)


def ValidatePlayers(players: list) -> list and list:
	errorMessages = []
	# Add players from players to validatedPlayers that aren't empty strings or duplicates
	validatedPlayers = []
	for player in players:
		player = player.strip()
		if player != '':
			# Remove non-alphanumeric chars from name
			# so it can be used in file naming
			alNumName = ''
			for char in player:
				if char.isalnum():
					alNumName += char
			# Keeps improperly entered names that
			# are only non-alphanumeric from being added
			# to validatedPlayers as empty strings
			if len(alNumName) < 1:
				errorMessages.append(f'Invalid player name which only contains special characters: {player}')
			if alNumName in validatedPlayers:
				errorMessages.append(f'Duplicate player found: {alNumName}.')
			if len(errorMessages) == 0:
				validatedPlayers.append(alNumName)
	return validatedPlayers, errorMessages





def main():
	version = "0.0.4"
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
	print('')
	while True:
		players = input('Enter list of people participating separated by commas. Note: special character will be removed.\n').split(',')
		validatedPlayers, errorMessages = ValidatePlayers(players)
		if len(errorMessages) > 0:
			print('')
			for message in errorMessages:
				print(message)
			errorMessages = []
		else:
			break


	totalPlayers = len(validatedPlayers)
	if totalPlayers < 4:
		input(f'A minimum of 4 players is required, & you entered {totalPlayers}. Please type "Enter" to exit then re-run script')
		sys.exit()



	## SCRIPT BODY ##
	PopulateGiversDictionary(givers, validatedPlayers)


	# Add all giver names to each giver then remove their own name & their last year receiver
	for giver in givers:
		AssignInitialReceivers(giver, givers, validatedPlayers, lastMatches)


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
			Restart(givers, validatedPlayers, lastMatches)
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
