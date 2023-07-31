from standings import*
from sleeper_wrapper import League, User, Stats, Players, Drafts

import json


players = Players()
stats = Stats()
league = League("851103743612141568")
drafts = Drafts("851103743612141568")

allRosters = league.get_rosters()  
allUsers = league.get_users()  
standingsData = league.get_standings(allRosters, allUsers)

rostersFile = json.dumps(allRosters,indent = 4, sort_keys= True)
with open("rostersfile.json","w") as outfile:
    outfile.write(rostersFile)

usersFile = json.dumps(allUsers,indent = 4, sort_keys= True)
with open("usersfile.json","w") as outfile:
    outfile.write(usersFile)

userNames = []

for roster in allRosters: #puts all usernames in a list using roster
    userID = roster["owner_id"]
    teamOwner = User(userID)
    userName = teamOwner.get_username()
    userNames.append(userName)

for name in userNames: #prints all usernames
    print(name)

#Return of league.get_standings(allRosters, league.get_users())
#[(teamName, number_of_wins, number_of_losses, total_points), 
# (teamName, number_of_wins, number_of_losses, total_points)]

print()

printStandings(standingsData, allRosters, allUsers)