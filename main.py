## GLOBAL VARIABLES ##
givers = {
    'Me': [],
    'Satoshi Nakamoto': [],
    'Aragorn': [],
    'Nacho Libre': [],
    "Li'l Sebastian": [],
    'Groot': [],
    'Brave Sir Robin': []
}
lastMatches = {
    'Me': 'Satoshi Nakamoto',
    'Aragorn': 'Nacho Libre',
    "Li'l Sebastian": 'Groot',
    'Groot': 'Brave Sir Robin',
    'Satoshi Nakamoto': 'Aragorn',
    'Nacho Libre': "Li'l Sebastian",
    'Brave Sir Robin': 'Me'
}


## Functions ##
def AssignInitialOptions():
    for giver, giverList in givers.items():
        # Add all names in givers list to each giver if they are initial receiver options
        for receiver, giverList in givers.items():
            # Excludes the giver themself & their last year receiver
            if receiver == giver or receiver == lastMatches[giver]:
                continue
            else:
                givers[giver].append(receiver)


def ReduceOptions():
    # Iterate thru givers
    for giver, receiverList in givers.items():
        # Iterate thru giver's reciever list
        for receiver in receiverList:
            if giver in givers[receiver]:
                givers[receiver].remove(giver)
                givers[giver].remove(receiver)
    CheckReceiverListLen()


# Repeats ReduceOptions() if any giver has more than 1 receiver
def CheckReceiverListLen():
    for giver, receiverList in givers.items():
        if len(receiverList) > 1:
            ReduceOptions()


## MAIN PROGRAM ##
# Receive input of giver names from user & populates givers{}
# GetGiverNames()

# Populates lastMatches{} with LastYearMatches.txt data
# PopulateLastMatches()

# Keeps givers from knowing who's buying for who if they know how the script works
# RandomizeGiversOrder()

# Assign each giver all names besides their own & the one they gifted last year
AssignInitialOptions()

ReduceOptions()

# UpdateLastYearMatches()

# Creates one file per giver named after the giver which contains their receiver's name
# CreateGiverFiles()

print(givers)