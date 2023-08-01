from sleeper_wrapper import League, User, Stats, Players, Drafts

#setter: sets all values needed to display
def set_total_values(standingsList: list, rosterList : list, userList: list):
    global myLeague

    myLeague = []
    
    seed = 1
    for teaminfo in standingsList:
        myLeagueData = {
            'seed' : '',
            'username' : '',
            'owner id' : '',
            'team name' : '',
            'record' : '',
            'wins' : '',
            'losses' : '',
            'ties' : '',
            'total games' : '',
            'win%' : '',
            'total FP' : '',
            'total opposing FP' : '',
            'total max FP' : '',
            'total game pick eff' : '',
            'power rank' : '',
            'avg pd' : ''
        }
        ties = 0
        totalMaxFP = 0 
        totalOppFP = 0
        
        teamName = teaminfo[0]
        myLeagueData['team name'] = teamName

        for j in range(len(userList)):
            currentUser = userList[j] 
            if currentUser["display_name"] == teamName:
                thisUser = User(currentUser["display_name"])
                myLeagueData['username'] = currentUser["display_name"]
                break
            try:
                if currentUser["metadata"]["team_name"] == teamName:
                    thisUser = User(currentUser["display_name"])
                    myLeagueData['username'] = currentUser["display_name"]
                    break
            except:
                continue
        
        thisUserID = thisUser.get_user_id()
        myLeagueData['owner id'] = thisUserID

        for i in range(len(rosterList)):
            currentRoster = rosterList[i]
            if currentRoster["owner_id"] == thisUserID:
                
                ties = currentRoster["settings"]["ties"]
                myLeagueData['ties'] = ties

                totalMaxFP_String = str(currentRoster["settings"]["ppts"] )
                totalOppFP_String = str(currentRoster["settings"]["fpts_against"])
                totalFP_decimalString = str(currentRoster["settings"]["fpts_decimal"])
                totalOppFP_decimalString = str(currentRoster["settings"]["fpts_against_decimal"])
                totalMaxFP_decimalString = str(currentRoster["settings"]["ppts_decimal"])
                break
        
        wins = int(teaminfo[1])
        myLeagueData['wins'] = wins

        losses = int(teaminfo[2])
        myLeagueData['losses'] = losses 

        record = str(wins) + " - " + str(losses) + " - " + str(ties)
        myLeagueData['record'] = record

        totalFP = float((teaminfo[3] + "." +totalFP_decimalString))
        myLeagueData['total FP'] = totalFP 

        totalMaxFP = float((totalMaxFP_String + "." + totalMaxFP_decimalString))
        myLeagueData['total max FP'] = totalMaxFP

        totalOppFP = float((totalOppFP_String + "." + totalOppFP_decimalString))
        myLeagueData['total opposing FP'] = totalOppFP 
        
        totalEfficiency = float((totalFP / totalMaxFP))*100
        myLeagueData['total game pick eff'] = totalEfficiency

        totalGames = wins + losses + ties
        myLeagueData['total games'] = totalGames

        winpercentage = float((2 * wins + ties) / (2 * totalGames))
        myLeagueData['win%'] = winpercentage

        powerRanking = float((totalFP * 2) + (totalFP * float(winpercentage)) + (totalFP * float(winpercentage)))
        myLeagueData['power rank'] = powerRanking 
        
        avgPointDiff = float(totalFP / totalGames) - float(totalOppFP / totalGames)
        myLeagueData['avg pd'] = avgPointDiff

        myLeagueData['seed'] = seed

        myLeague.append(myLeagueData)

        seed += 1

def sort_by_category(case, key):
    global globalKey, globalCase
    globalKey = key
    globalCase = case
    try:
        if case == 0:#low to high
            for i in range(1, len(myLeague)):
                thisLeague = myLeague[i]
                j = i - 1

                # Move elements that are greater than the thisLeague element to one position ahead
                # of their thisLeague position, based on the specified key value.
                while j >= 0 and thisLeague[key] < myLeague[j][key]:
                    myLeague[j + 1] = myLeague[j]
                    j -= 1

                # Insert the thisLeague element in its correct position
                myLeague[j + 1] = thisLeague

        if case == 1: #High to Low
            for i in range(1, len(myLeague)):
                thisLeague = myLeague[i]
                j = i - 1

                # Move elements that are smaller than the thisLeague element to one position ahead
                # of their thisLeague position, based on the specified key value.
                while j >= 0 and thisLeague[key] > myLeague[j][key]:
                    myLeague[j + 1] = myLeague[j]
                    j -= 1

                # Insert the thisLeague element in its correct position
                myLeague[j + 1] = thisLeague
    except: 
        print("ERROR: Invalid case/key parameter OR set_total_values not called!")
         
def display_standings():
        try:
            categories = {
            'win%' : "Record / Win Percentage / Seeding",
            'total FP' : "Total Scored FP",
            'total opposing FP' : "Total Opposing FP",
            'total max FP' : "Total Max FP",
            'total game pick eff' : "Game Pick Efficiency",
            'power rank' : "Power Ranking",
            'avg pd' : "Average Point Differential"
            }
            if globalCase == 0:
                print("[SELECTED SORT]: ASCENDING / LOW TO HIGH | [SELECTED CATEGORY]: " + categories[globalKey].upper())
                rank = 10
            elif globalCase == 1:
                print("[SELECTED SORT]: DESCENDING / HIGH TO LOW | [SELECTED CATEGORY]: " + categories[globalKey].upper())
                rank = 1
            for thisLeague in myLeague: 
                print("Seed " + str(thisLeague['seed']) + ": " + thisLeague['team name'])
                
                #only prints the specified ranked category set when sort_by is called
                if globalKey == 'win%':
                    print("\t|| Record: " + thisLeague['record']+ " / Win%: " + 
                    "{:.3f}".format(thisLeague['win%']).lstrip('0')+ " || [RANK: " + str(rank) +"]")           
                elif globalKey == 'total FP':
                    print("\t|| Total Scored FP: " + "{:.2f}".format(thisLeague['total FP'] +                                                              
                                                                    " || [RANK: " + str(rank) +"]"))            
                elif globalKey == 'total max FP':
                    print("\t|| Total Max FP: " + "{:.2f}".format(thisLeague['total max FP']) + 
                                                                " || [RANK: " + str(rank) +"]")
                elif globalKey == 'total game pick eff':
                    print("\t|| Game Pick Efficiency: " + "{:.2f}".format(thisLeague['total game pick eff']) + 
                                                                                "% || [RANK: " + str(rank) +"]")
                elif globalKey == 'power rank':
                    print("\t|| Power Ranking: " + "{:.2f}".format(thisLeague['power rank']) +
                                                                    " || [RANK: " + str(rank) +"]")
                elif globalKey == 'avg pd':
                    print("\t|| Average Point Differential: " + "{:.2f}".format(thisLeague['avg pd']) + 
                                                                " || [RANK: " + str(rank) +"]") 
                
                #will print all statements but the ranked category
                if globalKey != 'win%':
                    print("\tRecord: " + thisLeague['record']+ " / Win%: " + "{:.3f}".format(thisLeague['win%']).lstrip('0'))
                if globalKey != 'total FP':
                    print("\tTotal Scored FP: " + "{:.2f}".format(thisLeague['total FP']))
                if globalKey != 'total opposing FP':
                    print("\tTotal Opposing FP: " + "{:.2f}".format(thisLeague['total opposing FP'])) 
                if globalKey != 'total max FP':
                    print("\tTotal Max FP: " + "{:.2f}".format(thisLeague['total max FP']))
                if globalKey != 'total game pick eff': 
                    print("\tGame Pick Efficiency: " + "{:.2f}".format(thisLeague['total game pick eff']) + "%")             
                if globalKey != 'power rank':
                    print("\tPower Ranking: " + "{:.2f}".format(thisLeague['power rank']))           
                if globalKey != 'avg pd':
                    print("\tAverage Point Differential: " + "{:.2f}".format(thisLeague['avg pd'])) 
                
                # rank declines if descending and improves if ascending
                if globalCase == 0:
                    rank -= 1
                elif globalCase == 1:
                    rank += 1
        except:
            print("ERROR: Invalid category/case provided OR category not sorted!")