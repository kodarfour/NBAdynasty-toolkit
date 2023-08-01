from sleeper_wrapper import League, User, Stats, Players, Drafts

#setter: sets all values needed to display
def set_values(standingsList: list, rosterList : list, userList: list):
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

def sort_by_input(case, key):
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
        print("ERROR: Sorting gone wrong!!!")
         
def display_by_standing():
        rank = 1
        for thisLeague in myLeague: 
            print(str(thisLeague['seed']) + ": " + thisLeague['team name'])
            print("\t|| Record: " + thisLeague['record']+ " / Win%: " + 
                  "{:.3f}".format(thisLeague['win%']).lstrip('0')+ " || [RANK: " + str(rank) +"]")
            print("\tTotal Scored FP: " + "{:.2f}".format(thisLeague['total FP']))
            print("\tTotal Opposing FP: " + "{:.2f}".format(thisLeague['total opposing FP'])) 
            print("\tTotal Max FP: " + "{:.2f}".format(thisLeague['total max FP'])) 
            print("\tGame Pick Efficiency: " + "{:.2f}".format(thisLeague['total game pick eff']) + "%") 
            print("\tPower Ranking: " + "{:.2f}".format(thisLeague['power rank']))
            print("\tAVG Point Differential: " + "{:.2f}".format(thisLeague['avg pd'])) 
            rank += 1

def display_by_totalFP():
    rank = 1
    for thisLeague in myLeague: 
            print(str(thisLeague['seed']) + ": " + thisLeague['team name'])
            print("\t|| Total Scored FP: " + "{:.2f}".format(thisLeague['total FP'] + 
                                                             " || [RANK: " + str(rank) +"]"))
            print("\tRecord: " + thisLeague['record']+ " / Win%: " + "{:.3f}".format(thisLeague['win%']).lstrip('0'))
            print("\tTotal Opposing FP: " + "{:.2f}".format(thisLeague['total opposing FP'])) 
            print("\tTotal Max FP: " + "{:.2f}".format(thisLeague['total max FP'])) 
            print("\tGame Pick Efficiency: " + "{:.2f}".format(thisLeague['total game pick eff']) + "%") 
            print("\tPower Ranking: " + "{:.2f}".format(thisLeague['power rank']))
            print("\tAVG Point Differential: " + "{:.2f}".format(thisLeague['avg pd'])) 
            rank += 1

def display_by_totalMaxFP():
    rank = 1
    for thisLeague in myLeague: 
            print(str(thisLeague['seed']) + ": " + thisLeague['team name'])
            print("\t|| Total Max FP: " + "{:.2f}".format(thisLeague['total max FP']) + 
                                                            " || [RANK: " + str(rank) +"]")
            print("\tRecord: " + thisLeague['record']+ " / Win%: " + "{:.3f}".format(thisLeague['win%']).lstrip('0'))
            print("\tTotal Scored FP: " + "{:.2f}".format(thisLeague['total FP']))
            print("\tTotal Opposing FP: " + "{:.2f}".format(thisLeague['total opposing FP'])) 
            print("\tGame Pick Efficiency: " + "{:.2f}".format(thisLeague['total game pick eff']) + "%") 
            print("\tPower Ranking: " + "{:.2f}".format(thisLeague['power rank']))
            print("\tAVG Point Differential: " + "{:.2f}".format(thisLeague['avg pd'])) 
            rank += 1

def display_by_totalEfficiency():
    rank = 1
    for thisLeague in myLeague: 
            print(str(thisLeague['seed']) + ": " + thisLeague['team name'])
            print("\t|| Game Pick Efficiency: " + "{:.2f}".format(thisLeague['total game pick eff']) + 
                                                                            "% || [RANK: " + str(rank) +"]") 
            print("\tRecord: " + thisLeague['record']+ " / Win%: " + "{:.3f}".format(thisLeague['win%']).lstrip('0'))
            print("\tTotal Scored FP: " + "{:.2f}".format(thisLeague['total FP']))
            print("\tTotal Opposing FP: " + "{:.2f}".format(thisLeague['total opposing FP'])) 
            print("\tTotal Max FP: " + "{:.2f}".format(thisLeague['total max FP'])) 
            print("\tPower Ranking: " + "{:.2f}".format(thisLeague['power rank']))
            print("\tAVG Point Differential: " + "{:.2f}".format(thisLeague['avg pd'])) 
            rank += 1

def display_by_powerRank():
    rank = 1
    for thisLeague in myLeague: 
            print(str(thisLeague['seed']) + ": " + thisLeague['team name'])
            print("\t|| Power Ranking: " + "{:.2f}".format(thisLeague['power rank']) +
                                                                 " || [RANK: " + str(rank) +"]")
            print("\tRecord: " + thisLeague['record']+ " / Win%: " + "{:.3f}".format(thisLeague['win%']).lstrip('0'))
            print("\tTotal Scored FP: " + "{:.2f}".format(thisLeague['total FP']))
            print("\tTotal Opposing FP: " + "{:.2f}".format(thisLeague['total opposing FP'])) 
            print("\tTotal Max FP: " + "{:.2f}".format(thisLeague['total max FP'])) 
            print("\tGame Pick Efficiency: " + "{:.2f}".format(thisLeague['total game pick eff']) + "%") 
            print("\tAVG Point Differential: " + "{:.2f}".format(thisLeague['avg pd']))   
            rank += 1

def display_by_avgPD():
    rank = 1
    for thisLeague in myLeague: 
            print(str(thisLeague['seed']) + ": " + thisLeague['team name'])
            print("\t|| AVG Point Differential: " + "{:.2f}".format(thisLeague['avg pd']) + 
                                                            " || [RANK: " + str(rank) +"]") 
            print("\tRecord: " + thisLeague['record']+ " / Win%: " + "{:.3f}".format(thisLeague['win%']).lstrip('0'))
            print("\tTotal Scored FP: " + "{:.2f}".format(thisLeague['total FP']))
            print("\tTotal Opposing FP: " + "{:.2f}".format(thisLeague['total opposing FP'])) 
            print("\tTotal Max FP: " + "{:.2f}".format(thisLeague['total max FP'])) 
            print("\tGame Pick Efficiency: " + "{:.2f}".format(thisLeague['total game pick eff']) + "%") 
            print("\tPower Ranking: " + "{:.2f}".format(thisLeague['power rank']))
            rank += 1
            
