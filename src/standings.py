from sleeper_wrapper import League, User, Stats, Players, Drafts



def printStandings(standingsList: list, rosterList : list, userList: list):
    print("League Standings ")# add specific week 
    seed = 1
    for teaminfo in standingsList:
        ties = 0
        maxFP = 0 
        totalOppFP = 0
        teamName = teaminfo[0]
        for j in range(len(userList)):
            currentUser = userList[j] 
            if currentUser["display_name"] == teamName:
                owner = User(currentUser["display_name"])
                break
            try:
                if currentUser["metadata"]["team_name"] == teamName:
                    owner = User(currentUser["display_name"])
                    break
            except:
                continue
        
        ownerID = owner.get_user_id()

        for i in range(len(rosterList)):
            currentRoster = rosterList[i]
            if currentRoster["owner_id"] == ownerID:
                ties = currentRoster["settings"]["ties"]
                maxFP = currentRoster["settings"]["ppts"] 
                totalOppFP = currentRoster["settings"]["fpts_against"]
                break
        
        wins = int(teaminfo[1])
        losses = int(teaminfo[2])
        totalFP = int(teaminfo[3])
        efficiency = float("{:.3f}".format(totalFP / maxFP))*100
        totalGames = wins + losses + ties
        winpercentage = "{:.3f}".format((2 * wins + ties) / (2 * totalGames)) #NOTE THIS IS A STRING
        powerRanking = float("{:.2f}".format((totalFP * 2) + (totalFP * float(winpercentage)) + (totalFP * float(winpercentage))))
        avgPointDiff = float("{:.2f}".format(float(totalFP / totalGames) - float(totalOppFP / totalGames)))
        print(str(seed) + ": " + teamName)
        print("\tRecord: " + str(wins) + " - " + str(losses) + " - " + str(ties))
        print("\tWin%: " + winpercentage.lstrip('0'))
        print("\tTotal FP: " + str(totalFP))
        print("\tOpposing FP: " + str(totalOppFP)) 
        print("\tMax FP: " + str(maxFP)) 
        print("\tGame Pick Efficiency: " + str(efficiency) + "%") 
        print("\tPower Ranking: " + str(powerRanking)) 
        print("\tAVG Point Differential: " + str(avgPointDiff)) 
        seed += 1

        
    
