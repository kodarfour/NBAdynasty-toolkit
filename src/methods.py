from sleeper_wrapper import League, User, Stats, Players, Drafts
from backups import *
from datetime import datetime
import pandas as pd
from nba_api.stats.endpoints import playergamelog
import requests, time, json

#setter: sets all values needed to display
def set_total_values(standingsList: list, rosterList : list, userList: list, path : str, leagueID : str):
    global myLeague

    myLeague = []
    myLeagueWeekly = []
    
    seed = 1
    if check_tMyLeague():
        print("assigning tMyLeague data file...")
        myLeague = set_tMyLeague()
        print("assigned tMyLeagueData.json ✓✓✓")
    else:
        print("gathering and creating tMyLeague data file...")
        with open(path+"/"+"weeklycreationlog.txt","w") as f:
            f.write("LOG:\n")
            f.close()
        for teaminfo in standingsList: #gathers data for myLeague
            myLeagueData = {
                'seed' : None,
                'username' : None,
                'roster id' : None,
                'owner id' : None,
                'team name' : None,
                'record' : None,
                'wins' : None,
                'losses' : None,
                'ties' : None,
                'total games' : None,
                'win%' : None,
                'total FP' : None,
                'total opposing FP' : None,
                'total max FP' : None,
                'total game pick eff' : None,
                'power rank' : None,
                'avg pd' : None
            }
            ties = 0
            totalMaxFP = 0 
            totalOppFP = 0
            
            teamName = teaminfo[0]
            myLeagueData['team name'] = teamName

            for j in range(len(userList)): # opens user list
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

            for i in range(len(rosterList)): #opens rosterlist
                currentRoster = rosterList[i]
                if currentRoster["owner_id"] == thisUserID:
                    
                    rosterID = currentRoster["roster_id"]
                    myLeagueData["roster id"] = rosterID
                    
                    ties = currentRoster["settings"]["ties"]
                    myLeagueData['ties'] = ties -1
                    break
            
            wins = int(teaminfo[1])
            myLeagueData['wins'] = wins

            losses = int(teaminfo[2])
            myLeagueData['losses'] = losses 

            record = str(wins) + " - " + str(losses) + " - " + str(ties)
            myLeagueData['record'] = record

            realScoredFP = 0.00
            realAgainstFP = 0.00
            realMaxFP = 0.00
            for i in range(1,18): #adds up total scored for every week
                
                print("getting week", i, "data (total):",myLeagueData['username']+ "...")
                fp_results = get_weeklyFP_data(rosterID, i, path, leagueID, myLeagueData['username'])
                print("recieved week", i ,"data (total):", myLeagueData['username'], "✓✓✓")
                
                weekly_dict = {
                    "Team": myLeagueData['username'],
                    "Week" : i,
                    "FP For" : fp_results[0],
                    "FP Against" : fp_results[1],
                    "FP Max" : fp_results[2]
                }
                
                myLeagueWeekly.append(weekly_dict)
                
                realScoredFP += fp_results[0]
                realAgainstFP += fp_results[1]
                realMaxFP += fp_results[2]
            
            totalFP = float("{:.2f}".format(realScoredFP))
            myLeagueData['total FP'] = totalFP 
            
            totalOppFP = float("{:.2f}".format(realAgainstFP))
            myLeagueData['total opposing FP'] = totalOppFP 

            totalMaxFP = float("{:.2f}".format(realMaxFP))
            myLeagueData['total max FP'] = totalMaxFP
            
            totalEfficiency = float("{:.2f}".format(float((totalFP / totalMaxFP))*100))
            myLeagueData['total game pick eff'] = totalEfficiency

            totalGames = wins + losses + ties
            myLeagueData['total games'] = totalGames

            winpercentage = float("{:.3f}".format(float((2 * wins + ties) / (2 * totalGames))))
            myLeagueData['win%'] = winpercentage

            powerRanking = float("{:.2f}".format(float((totalFP * 2) + (totalFP * float(winpercentage)) + (totalFP * float(winpercentage)))))
            myLeagueData['power rank'] = powerRanking 
            
            avgPointDiff = float("{:.2f}".format(float(totalFP / totalGames) - float(totalOppFP / totalGames)))
            myLeagueData['avg pd'] = avgPointDiff

            myLeagueData['seed'] = seed

            myLeague.append(myLeagueData)

            seed += 1
        backup_tMyLeague(myLeague)
        backup_wMyLeague(myLeagueWeekly)
        print("created tMyLeagueData.json ✓✓✓")

def get_weeklyFP_data(rosterID : int, week : int, path : str, leagueID : str, username : str):
    
    scored = 0
    against = 0
    scored_max = 0
    maxList = [0]
    thisPlayersMaxList = []
    
    with open(path + "/matchupfile-" + leagueID + "-week" + str(week)+ ".json") as f:
        matchupData = json.load(f)
        f.close()
    
    with open(path + "/allplayersFormatted.json") as f:
        allPlayerData = json.load(f)
        f.close()
    
    week_range = get_week(week)
    
    for i in range(11): #iterates through every team
        if matchupData[i]["roster_id"] == rosterID:
            scored = matchupData[i]["points"]
            currentMatchupID = matchupData[i]["matchup_id"]
            for starter in matchupData[i]["starters"]: # parse through starter ids
                for index in range(len(allPlayerData)): # parse through all players
                    if starter == allPlayerData[index]["sleeper-player-id"]: # when we find matching players...
                        tripDub = 0
                        dubDub = 0
                        fortyBomb = 0
                        fiftyBomb = 0
                        fifteenAsts = 0
                        twentyRebs = 0
                        time.sleep(1) #so data doesnt get messed up
                        gamelog_thisPlayer = playergamelog.PlayerGameLog(
                            player_id=allPlayerData[index]["nba-api-pID"], 
                            season = '2022',
                            date_from_nullable =  week_range[0],
                            date_to_nullable = week_range[-1]
                        ).get_dict()
                        
                        with open(path+"/"+"weeklycreationlog.txt","a") as f:
                                f.write("\n\ncurrent user: " +  username + "\ncurrent player: " + allPlayerData[index]["player-name"] + "\ncurrent week:"+ str(week)+ "\n\n\n")
                                f.close()
                        
                        #Calculate fantasy score for each game played that week all below
                        for game in range(len(gamelog_thisPlayer["resultSets"][0]["rowSet"])):
                            pts = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][-3]
                            blks = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][-6]
                            stls = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][-7]
                            asts = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][-8]
                            rebs = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][-9]
                            orebs = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][-11]
                            threePM = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][-17]
                            tovs = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][-5]
                            pfs = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][-4]
                            
                            current_date = gamelog_thisPlayer["resultSets"][0]["rowSet"][game][3]
                            
                            basicStatsDict = {
                                "pts" : pts, 
                                "blks" : blks, 
                                "stls" : stls, 
                                "asts" : asts, 
                                "rebs" : rebs, 
                                "orebs": orebs, 
                                "threePM" : threePM, 
                                "tovs": tovs,
                                "pfs" : pfs
                            }
                            
                            tripDub += get_SpecialStats(basicStatsDict,"TD3")
                            dubDub += get_SpecialStats(basicStatsDict, "DD2")
                            fortyBomb += get_SpecialStats(basicStatsDict, "40+P")
                            fiftyBomb += get_SpecialStats(basicStatsDict, "50+P")
                            fifteenAsts += get_SpecialStats(basicStatsDict, "15+A")
                            twentyRebs += get_SpecialStats(basicStatsDict, "20+R")
                            
                            allStatsDict = {
                                "pts" : pts, 
                                "blks" : blks, 
                                "stls" : stls, 
                                "asts" : asts, 
                                "rebs" : rebs, 
                                "orebs": orebs, 
                                "threePM" : threePM, 
                                "tovs": tovs,
                                "pfs" : pfs,
                                "TD3" : tripDub,
                                "DD2" : dubDub,
                                "40+P" : fortyBomb,
                                "50+P" : fiftyBomb,
                                "15+A" : fifteenAsts,
                                "20+R" : twentyRebs
                            }
                            
                            fantasyScore = round(boxscore_to_FPboxscore(allStatsDict), 2)
                            
                            with open(path+"/"+"weeklycreationlog.txt","a") as f:
                                f.write(allPlayerData[index]["player-name"] + " scored " + str(fantasyScore) + " on "+ current_date+ "\n")
                                f.close()
                            
                            thisPlayersMaxList.append(fantasyScore) # add to list of scores for the specified player
                            
                            with open(path+"/"+"weeklycreationlog.txt","a") as f:
                                f.write(allPlayerData[index]["player-name"] + " current listed games " + str(thisPlayersMaxList) + " for week range: " + week_range[0]+ "-" + week_range[-1]+ "\n")
                                f.close()
                        
                        try:
                            maxList.append(max(thisPlayersMaxList) + (allPlayerData[index]["TFPG"] * -1))
                            
                            with open(path+"/"+"weeklycreationlog.txt","a") as f:
                                f.write(allPlayerData[index]["player-name"] + " max score for week range " + week_range[0]+ "-" + week_range[-1] + " is: "+  str(max(thisPlayersMaxList)) + "\n")
                                f.close()   
                            
                            thisPlayersMaxList = []
                        except:
                            maxList.append(0)
                            
                            with open(path+"/"+"weeklycreationlog.txt","a") as f:
                                f.write(allPlayerData[index]["player-name"] + " max score for week range " + week_range[0]+ "-" + week_range[-1] + " is: 0\n")
                                f.close()
                            
                            thisPlayersMaxList = []
            break
    
    scored_max = round(sum(maxList), 2)
    
    for j in range(11):
        if (matchupData[j]["matchup_id"] == currentMatchupID) and (matchupData[j]["roster_id"] != rosterID):
        #if the matchup id matches and  the roster ID isn't the current team we are parsing...
            against = matchupData[j]["points"]
            break
    
    return [scored, against, scored_max]

def get_week(week_num):
    D = 'D'
    week_dict = {
        1 : ["10/18/2022","10/23/2022"],
        2 : ["10/24/2022", "10/30/2022"],
        3 : ["10/31/2022", "11/06/2022"],
        4 : ["11/07/2022", "11/13/2022"],
        5 : ["11/14/2022", "11/20/2022"],
        6 : ["11/21/2022", "11/27/2022"],
        7 : ["11/28/2022", "12/04/2022"],
        8 : ["12/05/2022", "12/11/2022"],
        9 : ["12/12/2022", "12/18/2022"],
        10 : ["12/19/2022", "12/25/2022"],
        11 : ["12/26/2022", "01/01/2023"],
        12 : ["01/02/2023", "01/08/2023"],
        13 : ["01/09/2023", "01/15/2023"],
        14 : ["01/16/2023", "01/22/2023"],
        15 : ["01/23/2023", "01/29/2023"],
        16 : ["01/30/2023", "02/05/2023"],
        17 : ["02/06/2023", "02/12/2023"]
    }
    
    start_date = datetime.strptime(week_dict[week_num][0], "%m/%d/%Y")
    end_date = datetime.strptime(week_dict[week_num][1], "%m/%d/%Y")

    week_range = pd.date_range(start_date, end_date, freq=D)
    week_range = week_range.strftime("%m/%d/%Y")
    week_range = week_range.values.tolist()
    
    return week_range

def get_SpecialStats(
    allBasicStats = {
                "pts" : 0, 
                "blks" : 0, 
                "stls" : 0, 
                "asts" : 0, 
                "rebs" : 0, 
                "orebs": 0, 
                "threePM" : 0, 
                "tovs": 0,
                "pfs" : 0
            }, 
        category = str
):
    #50+ pts
    if category == "50+P":
        if(allBasicStats["pts"] >= 50):
            return  1
        else:
            return 0
        
    #40+ pts
    if category == "40+P":
        if(allBasicStats["pts"] >= 40):
            return 1
        else:
            return 0
        
    #15+ assists
    if category == "15+A":
        if(allBasicStats["asts"] >= 15):
            return 1
        else:
            return 0
    
    #20+ rebounds
    if category == "20+R":
        if(allBasicStats["rebs"] >= 20):
            return 1
        else:
            return 0
    
    #double doubles
    if category == "DD2":
        if(
            (allBasicStats["pts"] >= 10 and allBasicStats["rebs"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["asts"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["stls"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["blks"] >= 10) or
            (allBasicStats["rebs"] >= 10 and allBasicStats["asts"] >= 10) or
            (allBasicStats["rebs"] >= 10 and allBasicStats["stls"] >= 10) or
            (allBasicStats["rebs"] >= 10 and allBasicStats["blks"] >= 10) or
            (allBasicStats["asts"] >= 10 and allBasicStats["stls"] >= 10) or
            (allBasicStats["asts"] >= 10 and allBasicStats["blks"] >= 10) or
            (allBasicStats["stls"] >= 10 and allBasicStats["blks"] > 10)
        ):
            return 1
        else:
            return 0
    
    #triple doubles
    # pts >= 10
    # rebs >= 10
    # asts >= 10
    # stls >= 10
    # blks >= 10
    if category == "TD3":
        if(
            (allBasicStats["pts"] >= 10 and allBasicStats["rebs"] >= 10 and allBasicStats["asts"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["rebs"] >= 10 and allBasicStats["stls"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["rebs"] >= 10 and allBasicStats["blks"] >= 10) or
            (allBasicStats["rebs"] >= 10 and allBasicStats["asts"] >= 10 and allBasicStats["stls"] >= 10) or
            (allBasicStats["rebs"] >= 10 and allBasicStats["asts"] >= 10 and allBasicStats["blks"] >= 10) or
            (allBasicStats["asts"] >= 10 and allBasicStats["stls"] >= 10 and allBasicStats["blks"] >= 10) 
        ):
            return 1
        else:
            return 0

def boxscore_to_FPboxscore(
    allStats = {
        "pts" : 0, 
        "blks" : 0, 
        "stls" : 0, 
        "asts" : 0, 
        "rebs" : 0, 
        "orebs": 0, 
        "threePM" : 0, 
        "tovs": 0,
        "pfs" : 0,
        "TD3" : 0,
        "DD2" : 0,
        "40+P" : 0,
        "50+P" : 0,
        "15+A" : 0,
        "20+R" : 0
    }
):
    return (
        allStats["pts"] +
        (allStats["rebs"] * 1.15) +
        (allStats["asts"] * 1.7)  +
        (allStats["stls"] * 2)  +
        (allStats["blks"] * 2.7)  +
        (allStats["tovs"] * -1)  +
        (allStats["DD2"] * 2)  +
        (allStats["TD3"] * 3.5)  +
        (allStats["pfs"] * -0.15)  +
        (allStats["threePM"]* 0.5)  +
        (allStats["orebs"] * 0.5)  +
        (allStats["40+P"] * 3)  +
        (allStats["50+P"] * 5)  +
        (allStats["15+A"] * 4)  +
        (allStats["20+R"]* 5)  
    )
    