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
    
    seed = 1
    if check_tMyLeague():
        print("assigning tMyLeague data file...")
        myLeague = set_tMyLeague()
        print("assigned tMyLeagueData.json ✓✓✓")
    else:
        print("gathering and creating tMyLeague data file...")
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
                    myLeagueData['ties'] = ties
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
                realScoredFP += get_weeklyFP_data(rosterID, i, path, leagueID)[0]
                realAgainstFP += get_weeklyFP_data(rosterID, i, path, leagueID)[1]
                realMaxFP == get_weeklyFP_data(rosterID, i, path, leagueID)[2]
            
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
        print("created tMyLeagueData.json ✓✓✓")

def get_weeklyFP_data(rosterID : int, week : int, path : str, leagueID : str):
    scored = 0
    against = 0
    scored_max = 0
    maxList = []
    tripDub = 0
    dubDub = 0
    fortyBomb = 0
    fiftyBomb = 0
    fifteenAsts = 0
    twentyRebs = 0
    
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
                thisPlayersMaxList = []
                for index in range(len(allPlayerData)): # parse through all players
                    if starter == allPlayerData[index]["sleeper-player-id"]: # when we find matching players...
                        time.sleep(1) #so data doesnt get messed up
                        gamelog_thisPlayer = playergamelog.PlayerGameLog(
                            player_id=allPlayerData[index]["nba-api-pID"], 
                            season = '2022',
                            date_from_nullable =  week_range[0],
                            date_to_nullable = week_range[-1]
                        ).get_dict()
                        
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
                            
                            fantasyScore = boxscore_to_FPboxscore(allStatsDict)
                            thisPlayersMaxList.append(fantasyScore) # add to list of scores for the specified player
                        
                        maxList.append(max(thisPlayersMaxList))       
            break
    
    scored_max = sum(maxList)
    
    for j in range(11):
        if (matchupData[j]["matchup_id"] == currentMatchupID) and (matchupData[j]["roster_id"] != rosterID):
        #if the matchup id matches and  the roster ID isn't the current team we are parsing...
            against = matchupData[j]["points"]
            break
    
    return [scored, against, scored_max]

def get_week(week_num):
    D = 'D'
    week_dict = {
        1 : ["2022-10-18","2022-10-23"],
        2 : ["2022-10-24", "2022-10-30"],
        3 : ["2022-10-31", "2022-11-06"],
        4 : ["2022-10-07", "2022-11-06"],
        5 : ["2022-11-14", "2022-11-13"],
        6 : ["2022-11-21", "2022-11-27"],
        7 : ["2022-11-28", "2022-12-04"],
        8 : ["2022-12-05", "2022-12-11"],
        9 : ["2022-12-12", "2022-12-18"],
        10 : ["2022-12-19", "2022-12-25"],
        11 : ["2022-12-26", "2023-01-01"],
        12 : ["2023-01-02", "2023-01-08"],
        13 : ["2023-01-09", "2023-01-15"],
        14 : ["2023-01-16", "2023-01-22"],
        15 : ["2023-01-23", "2023-01-29"],
        16 : ["2023-01-30", "2023-02-05"],
        17 : ["2023-02-06", "2023-02-12"]
    }
    
    start_date = datetime.strptime(week_dict[week_num][0], "%Y-%m-%d")
    end_date = datetime.strptime(week_dict[week_num][1], "%Y-%m-%d")

    week_range = pd.date_range(start_date, end_date, freq=D)
    week_range = week_range.strftime("%Y-%m-%d")
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
        if(allBasicStats["reb"] >= 20):
            return 1
        else:
            return 0
    
    #double doubles
    if category == "DD2":
        if(
            (allBasicStats["pts"] >= 10 and allBasicStats["reb"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["asts"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["stls"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["blks"] >= 10) or
            (allBasicStats["reb"] >= 10 and allBasicStats["asts"] >= 10) or
            (allBasicStats["reb"] >= 10 and allBasicStats["stls"] >= 10) or
            (allBasicStats["reb"] >= 10 and allBasicStats["blks"] >= 10) or
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
            (allBasicStats["pts"] >= 10 and allBasicStats["reb"] >= 10 and allBasicStats["asts"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["reb"] >= 10 and allBasicStats["stls"] >= 10) or
            (allBasicStats["pts"] >= 10 and allBasicStats["reb"] >= 10 and allBasicStats["blks"] >= 10) or
            (allBasicStats["reb"] >= 10 and allBasicStats["asts"] >= 10 and allBasicStats["stls"] >= 10) or
            (allBasicStats["reb"] >= 10 and allBasicStats["asts"] >= 10 and allBasicStats["blks"] >= 10) or
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
    fp_total = (
        "pts" +
        ("rebs" * 1.15) +
        ("asts" * 1.7)  +
        ("stls" * 2)  +
        ("blks" * 2.7)  +
        ("tovs" * -1)  +
        ("DD2" * 2)  +
        ("TD3" * 3.5)  +
        ("pfs" * -0.15)  +
        ("threePM"* 0.5)  +
        ("orebs" * 0.5)  +
        ("40+P" * 3)  +
        ("50+P" * 5)  +
        ("15+A" * 4)  +
        ("20+R" * 5)  
    )
    
    return fp_total