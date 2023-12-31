import os
from pathlib import Path
import time, json, requests
from methods import *
from flask import *
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd
#create backups directory

def create_backups_dir(p):
    global path
    path = p 
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)
            raise

def check_allPlayersFile():
    global ap_fileName
    ap_fileName = "allplayersFormatted.json"
    obj = Path(path+"/"+ap_fileName)
    return obj.exists()

def backup_allPlayersFile():
    ap_fileName = "allplayersFormatted.json"
    ap_filePath = os.path.join(path, ap_fileName)
    data = requests.get('https://api.sleeper.app/v1/players/nba')
    print(data)
    if data.status_code == 200:
        
        url = 'https://www.teamrankings.com/nba/player-stat/fouls-technical?rate=season-totals&season_id=220'
        technicalFouls_df = pd.read_html(url)[0]
        technicalFouls_df = technicalFouls_df[["Player", "Value"]]
        
        with open(path+"/"+"allplayersFailLog.txt","w") as f:
            f.write("LOG:"+"\n")
            f.close()
        
        print("requesting all player data from Sleeper API...")
        rawJSON = data.json()
        playerList = []

        for playerInfo_tag in rawJSON.keys():
            innerDict = rawJSON[playerInfo_tag]
            playerDict = {
                    "sleeper-player-id": None,
                    "player-name": None,
                    "Team" : None,
                    "Age" : None,
                    "Pos 1" : None,
                    "Pos 2" : None,
                    "Pos 3" : None,
                    "FP-AVG" : None,
                    "FP-TOTAL" : None,
                    "GP" : None,
                    "MPG" : None,
                    "PPG" : None,
                    "RPG" : None,
                    "APG" : None,
                    "3PMPG" : None,
                    "OREBPG" : None,
                    "DREBPG" : None,
                    "BPG" : None,
                    "SPG" : None,
                    "TPG" : None,
                    "PFPG" : None,
                    "TFPG" : None,
                    "DD2PG" : None,
                    "TD3PG" : None,
                    "40+PPG": None,
                    "50+PPG": None,
                    "15+APG": None,
                    "20+RPG" : None,
                    "bdl-player-id" : None,
                    "nba-api-pID" : None
                }
            if (innerDict["active"] and innerDict["team"] is not None): #if player IS active AND IS on a team
                try:
                    test_if_playerID_is_Integer = int(playerInfo_tag) #if ID is an integer, go as planned
                    playerDict["sleeper-player-id"] = playerInfo_tag
                    playerDict["Team"] = innerDict['team']
                    playerDict["Age"] = innerDict['age']
                    playerDict["player-name"] = innerDict['full_name']
                        
                    for i in range(len(innerDict["fantasy_positions"])): #iterates through all position
                        try:
                            posNum = str((i+1))
                            playerDict["Pos " + posNum] = innerDict['fantasy_positions'][i] 
                            # sets fantasy position at playerDict key, 
                        except: 
                            break # if no position at index it stops running
                    
                    try:
                        get_bdl_playerData = requests.get("https://www.balldontlie.io/api/v1/players/?search=" + playerDict["player-name"])
                        if get_bdl_playerData.status_code == 200:
                            bdl_playerData = get_bdl_playerData.json()
                            bdl_playerID = bdl_playerData["data"][0]["id"]
                        time.sleep(1.3) #NOTE NEEDED IN BECAUSE THERE IS AN API CALL THROTTLE
                        get_bdl_playerAverages = requests.get("https://www.balldontlie.io/api/v1/season_averages?season=2022&player_ids[]="+str(bdl_playerID))
                        if get_bdl_playerAverages.status_code == 200:
                            averagesData = get_bdl_playerAverages.json()
                        onlyStats = averagesData["data"][0]
                        time.sleep(1.3) #NOTE NEEDED IN BECAUSE THERE IS AN API CALL THROTTLE
                        
                        if(len(onlyStats["min"]) == 4):
                            length = len(onlyStats["min"])
                            fullMinutes = float(onlyStats["min"][0])
                            lastTwo = (onlyStats["min"][length - 2])
                            decimal = float("0."+ lastTwo)
                            finalMinutes = fullMinutes + decimal
                        elif(len(onlyStats["min"]) == 5):
                            length = len(onlyStats["min"])
                            fullMinutes = float(onlyStats["min"][0:2])
                            lastTwo = (onlyStats["min"][length - 2])
                            decimal = float("0."+ lastTwo)
                            finalMinutes = fullMinutes + decimal
                        
                        playerDict["GP"] = onlyStats["games_played"]
                        playerDict["MPG"] = finalMinutes
                        playerDict["RPG"] = onlyStats["reb"]
                        playerDict["APG"] = onlyStats["ast"]
                        playerDict["3PMPG"] = onlyStats["fg3m"]
                        playerDict["OREBPG"] = onlyStats["oreb"]
                        playerDict["DREBPG"] = onlyStats["dreb"]
                        playerDict["BPG"] = onlyStats["blk"]
                        playerDict["SPG"] = onlyStats["stl"]
                        playerDict["TPG"] = onlyStats["turnover"]
                        playerDict["PFPG"] = onlyStats["pf"]
                        playerDict["PPG"] = onlyStats["pts"]
                        playerDict["bdl-player-id"] = onlyStats["player_id"]
                        
                        print("SUCCESS: BALLDONTLIE API 2022-2023 season stat average backed up! ✓✓✓ "+ playerDict["player-name"])
                        try:
                            playerDict["nba-api-pID"] = players.find_players_by_full_name(playerDict["player-name"])[0]['id']
                            
                            playerDict["40+PPG"] = 0
                            playerDict["50+PPG"] = 0
                            playerDict["15+APG"] = 0
                            playerDict["20+RPG"] = 0
                            playerDict["DD2PG"] = 0
                            playerDict["TD3PG"] = 0
                            playerDict["TFPG"] = 0
                            
                            gamelog_thisPlayer = playergamelog.PlayerGameLog(player_id=playerDict["nba-api-pID"], season = '2022').get_dict()
                            time.sleep(.5)
                            for i in range(len(gamelog_thisPlayer["resultSets"][0]["rowSet"])):
                                pts = gamelog_thisPlayer["resultSets"][0]["rowSet"][i][-3]
                                blks = gamelog_thisPlayer["resultSets"][0]["rowSet"][i][-6]
                                stls = gamelog_thisPlayer["resultSets"][0]["rowSet"][i][-7]
                                asts = gamelog_thisPlayer["resultSets"][0]["rowSet"][i][-8]
                                rebs = gamelog_thisPlayer["resultSets"][0]["rowSet"][i][-9]
                                
                                
                                #50+ pts
                                if(pts >= 50):
                                    playerDict["40+PPG"] += 1
                                    playerDict["50+PPG"] += 1
                                #or 40+ pts
                                elif(pts >= 40):
                                    playerDict["40+PPG"] += 1
                                    
                                #15+ assists
                                if(asts >= 15):
                                    playerDict["15+APG"] += 1
                                
                                #20+ rebounds
                                if(rebs >= 20):
                                    playerDict["20+RPG"] += 1
                                
                                #double doubles
                                if(
                                    (pts >= 10 and rebs >= 10) or
                                    (pts >= 10 and asts >= 10) or
                                    (pts >= 10 and stls >= 10) or
                                    (pts >= 10 and blks >= 10) or
                                    (rebs >= 10 and asts >= 10) or
                                    (rebs >= 10 and stls >= 10) or
                                    (rebs >= 10 and blks >= 10) or
                                    (asts >= 10 and stls >= 10) or
                                    (asts >= 10 and blks >= 10) or
                                    (stls >= 10 and blks > 10)
                                ):
                                    playerDict["DD2PG"] += 1
                                
                                #triple doubles 
                                
                                if(
                                    (pts >= 10 and rebs >= 10 and asts >= 10) or
                                    (pts >= 10 and rebs >= 10 and stls >= 10) or
                                    (pts >= 10 and rebs >= 10 and blks >= 10) or
                                    (rebs >= 10 and asts >= 10 and stls >= 10) or
                                    (rebs >= 10 and asts >= 10 and blks >= 10) or
                                    (asts >= 10 and stls >= 10 and blks >= 10) 
                                ):
                                    playerDict["TD3PG"] += 1
                            
                            
                            
                            if(playerDict["player-name"] in technicalFouls_df.values):
                                playertechs_df = technicalFouls_df[(technicalFouls_df["Player"] == playerDict["player-name"])]
                                playerDict["TFPG"] = playertechs_df.at[playertechs_df.index[0],"Value"]
                                

                            fp_total = (
                                (playerDict["PPG"] * playerDict["GP"]) +
                                ((playerDict["RPG"] * playerDict["GP"]) * 1.15) +
                                ((playerDict["APG"] * playerDict["GP"]) * 1.7)  +
                                ((playerDict["SPG"] * playerDict["GP"]) * 2)  +
                                ((playerDict["BPG"] * playerDict["GP"]) * 2.7)  +
                                ((playerDict["TPG"] * playerDict["GP"]) * -1)  +
                                (playerDict["DD2PG"] * 2)  +
                                (playerDict["TD3PG"] * 3.5)  +
                                ((playerDict["PFPG"] * playerDict["GP"]) * -0.15)  +
                                ((playerDict["3PMPG"] * playerDict["GP"]) * 0.5)  +
                                ((playerDict["OREBPG"] * playerDict["GP"]) * 0.5)  +
                                (playerDict["40+PPG"] * 3)  +
                                (playerDict["50+PPG"] * 5)  +
                                (playerDict["15+APG"] * 4)  +
                                (playerDict["20+RPG"] * 5)  +
                                (playerDict["TFPG"] * -1)
                            )
                            
                            playerDict["FP-TOTAL"] = fp_total
                            playerDict["FP-AVG"] = float(fp_total / playerDict["GP"])
                            
                            playerDict["40+PPG"] /= playerDict["GP"]
                            playerDict["50+PPG"] /= playerDict["GP"]
                            playerDict["15+APG"] /= playerDict["GP"]
                            playerDict["20+RPG"] /= playerDict["GP"]
                            playerDict["DD2PG"] /= playerDict["GP"]
                            playerDict["TD3PG"] /= playerDict["GP"]
                            playerDict["TFPG"] /= playerDict["GP"]
                            
                            print("SUCCESS: NBA API 2022-2023 \"remainder\" stats backed up ✓✓✓ " + playerDict["player-name"])
                        except:
                            time.sleep(1.3)
                            with open(path+"/"+"allplayersFailLog.txt","a") as f:
                                f.write("ERROR: NBA API 2022-2023 \"remainder\" stats back up failed! " + playerDict["player-name"]+"\n")
                                f.close()
                            print("ERROR: NBA API 2022-2023 \"remainder\" stats back up failed! " + playerDict["player-name"])
                        
                    except:
                        time.sleep(1.3)
                        with open(path+"/"+"allplayersFailLog.txt","a") as f:
                                f.write("ERROR: BALLDONTLIE API 2022-2023 season stat average back up failed! " + playerDict["player-name"]+"\n")
                                f.close()
                        print("ERROR: BALLDONTLIE API 2022-2023 season stat average back up failed! " + playerDict["player-name"])
                    finally:
                        playerList.append(playerDict)
                except: # if not an integer go to next dict
                    continue
        
        print("recieved all player data from Sleeper API ✓✓✓")
        newJSON = json.dumps(playerList ,indent = 2)
        
        if os.path.exists (path):
            print("creating/updating all players file...")
            with open(ap_filePath, "w") as f:
                f.write(newJSON)
            print("created/updated " + ap_fileName + " ✓✓✓")
    else:
        print("ERROR: Invalid Response Code (not 200)!!!")

def check_leagueID(leagueID):
    global leagueID_fileName
    global league_ID
    league_ID = leagueID
    leagueID_fileName = "leagueID-"+ leagueID+".txt"
    obj = Path(path+"/"+leagueID_fileName)
    return obj.exists()

def backup_leagueID(leagueID):
    leagueID_fileName = "leagueID-"+ leagueID+".txt"
    leagueID_filePath = os.path.join(path, leagueID_fileName)
    if os.path.exists (path):
        print("creating leagueID file...")
        with open(leagueID_filePath, "w") as f:
            f.write(leagueID)
        print("created " +leagueID_fileName + " ✓✓✓")

def check_rostersfile():
    global r_fileName
    r_fileName = "rostersfile-" + league_ID +".json"
    obj = Path(path+"/"+r_fileName)
    return obj.exists()
    
def backup_rostersfile(data):
    r_fileName = "rostersfile-" + league_ID +".json"
    r_filePath = os.path.join(path, r_fileName)
    newJSON = json.dumps(data, indent  = 2)
    if os.path.exists(path):
        print("creating rosters file...")
        with open(r_filePath, "w") as f:
            f.write(newJSON)
        print("created " + r_fileName + " ✓✓✓")

def set_rostersfile():
    r_fileName = "rostersfile-" + league_ID +".json"
    r_filePath = os.path.join(path, r_fileName)
    print("assigning rostersfile data...")
    with open(r_filePath) as newJSON:
        result = json.load(newJSON)
    print("assigned " + r_fileName + " ✓✓✓")
    return result
    
def check_usersfile():
    global u_fileName
    u_fileName = "usersfile-" + league_ID +".json"
    obj = Path(path+"/"+u_fileName)
    return obj.exists()

def backup_usersfile(data):
    u_fileName = "usersfile-" + league_ID +".json"
    u_filePath = os.path.join(path, u_fileName)
    newJSON = json.dumps(data,indent  = 2)
    if os.path.exists(path):
        print("creating users file...")
        with open(u_filePath, "w") as f:
            f.write(newJSON)
        print("created " + u_fileName + " ✓✓✓")

def set_usersfile():
    u_fileName = "usersfile-" + league_ID +".json"
    u_filePath = os.path.join(path, u_fileName)
    print("assigning usersfile data...")
    with open(u_filePath) as newJSON:
        result = json.load(newJSON)
    print("assigned " + u_fileName + " ✓✓✓")
    return result

def check_standingsfile():
    global s_fileName
    s_fileName = "standingsfile-" + league_ID +".json"
    obj = Path(path+"/"+s_fileName)
    return obj.exists()

def backup_standingsfile(data):
    s_fileName = "standingsfile-" + league_ID +".json"
    s_filePath = os.path.join(path, s_fileName)
    newJSON = json.dumps(data,indent  = 2)
    if os.path.exists(path):
        print("creating standings file...")
        with open(s_filePath, "w") as f:
            f.write(newJSON)
        print("created " + s_fileName + " ✓✓✓")

def set_standingsfile():
    s_fileName = "standingsfile-" + league_ID +".json"
    s_filePath = os.path.join(path, s_fileName)
    print("assigning standingsfile data...")
    with open(s_filePath) as newJSON:
        result = json.load(newJSON)
    print("assigned " + s_fileName + " ✓✓✓")
    return result

def check_matchupsfile(num):
    global m_fileName
    m_fileName = "matchupfile-" + league_ID + "-week"+str(num)+".json"
    obj = Path(path+"/"+m_fileName)
    return obj.exists()

def backup_matchupsfile(data, num):
    m_fileName = "matchupfile-" + league_ID + "-week"+str(num)+".json"
    m_filePath = os.path.join(path, m_fileName)
    newJSON = json.dumps(data,indent = 2)
    if os.path.exists(path):
        print("creating matchups file...")
        with open(m_filePath, "w") as f:
            f.write(newJSON)
        print("created " + m_fileName + " ✓✓✓")

def set_matchupsfile(num):
    m_fileName = "matchupfile-" + league_ID + "-week"+str(num)+".json"
    m_filePath = os.path.join(path, m_fileName)
    print("assigning matchupsfile data...")
    with open(m_filePath) as newJSON:
        result = json.load(newJSON)
    print("assigned " + m_fileName + " ✓✓✓")
    return result

def check_tMyLeague():
    global tMyLeague_fileName
    tMyLeague_fileName = "tMyLeagueData-" + league_ID +".json"
    obj = Path(path+"/"+tMyLeague_fileName)
    return obj.exists()

def backup_tMyLeague(data): #t is for total
    tMyLeague_fileName = "tMyLeagueData-" + league_ID +".json"
    tMyLeague_filePath = os.path.join(path, tMyLeague_fileName)
    newJSON = json.dumps(data,indent  = 2)
    if os.path.exists(path):
        with open(tMyLeague_filePath, "w") as f:
            f.write(newJSON)

def set_tMyLeague():
    tMyLeague_fileName = "tMyLeagueData-" + league_ID +".json"
    tMyLeague_filePath = os.path.join(path, tMyLeague_fileName)
    with open(tMyLeague_filePath) as newJSON:
        return  json.load(newJSON)

def check_df_leagueStandings():
    global dfLS_fileName
    dfLS_fileName = "df_leagueStandings-" + league_ID
    dfLS_filePath = path + "/" + dfLS_fileName + ".pkl"
    obj = Path(dfLS_filePath)
    return obj.exists()

def backup_df_leagueStandings():
    dfLS_fileName = "df_leagueStandings-" + league_ID
    dfLS_filePath = path + "/" + dfLS_fileName + ".pkl"
    
    format_leagueStandings = [
                    "Overall Fantasy Points Scored (FOR):", 
                    "Overall Fantasy Points Potentially Scored (FOR):", 
                    "Overall Fantasy Points Scored (AGAINST):",
                    "Game Pick Efficiency:", 
                    "Power Rank Score:"
                    ]
    
    print("creating and pickling league standings dataframe ...")
    
    leagueStandings = pd.read_json(path+ "/tMyLeagueData-" + league_ID + ".json")

    leagueStandings = leagueStandings.rename(columns= {
                                    "seed" : "Seed:",
                                    "username" : "Team Owner:", 
                                    "team name" : "Team:", 
                                    "record" : "Record:", 
                                    "wins" : "Wins:", 
                                    "losses" : "Losses:", 
                                    "ties" : "Ties:", 
                                    "win%" : "Win Percentage:", 
                                    "total FP" : "Overall Fantasy Points Scored (FOR):", 
                                    "total max FP" : "Overall Fantasy Points Potentially Scored (FOR):", 
                                    "total opposing FP" : "Overall Fantasy Points Scored (AGAINST):",
                                    "total game pick eff" : "Game Pick Efficiency:", 
                                    "power rank" : "Power Rank Score:", 
                                    "avg pd" : "Average Point Differential:"
                                    })

    leagueStandings = leagueStandings.drop(columns= ["roster id", "owner id", "total games"])

    leagueStandings = leagueStandings.set_index("Seed:")

    for column in format_leagueStandings:
        if column == "Game Pick Efficiency:":
            leagueStandings[column] = leagueStandings[column].map('{:.2f}'.format)
        else:
            leagueStandings[column] = leagueStandings[column].map('{:.2f}'.format)
            
    conversion = {
        "Overall Fantasy Points Scored (FOR):" : float, 
        "Overall Fantasy Points Potentially Scored (FOR):" : float, 
        "Overall Fantasy Points Scored (AGAINST):" : float,
        "Game Pick Efficiency:" : float, 
        "Power Rank Score:" : float
    }

    leagueStandings = leagueStandings.astype(conversion)
    
    leagueStandings.to_pickle(dfLS_filePath)
    
    print("created and pickled " + dfLS_fileName + ".pkl ✓✓✓")  

def check_df_playerPlayground():
    dfPP_fileName = "df_playerPlayground-" + league_ID
    dfPP_filePath = path + "/" + dfPP_fileName + ".pkl"
    
    obj = Path(dfPP_filePath)
    return obj.exists()

def backup_df_playerPlayground():
    
    dfPP_fileName = "df_playerPlayground-" + league_ID
    dfPP_filePath = path + "/" + dfPP_fileName + ".pkl"
    
    format_playerPlayground = [
            "Fantasy Points Per Game",
            'Position Rating',
            'Games Played',
            "Overall Fantasy Points Scored",
            "Points Per Game",
            "Rebounds Per Game",
            "Assists Per Game",
            "Made 3s Per Game",
            "Offensive Rebounds Per Game",
            "Defensive Rebounds Per Game",
            "Blocks Per Game",
            "Steals Per Game",
            "Turnovers Per Game",
            "Personal Fouls Per Game"
        ]

    print("creating and pickling player playground dataframe ...")
    
    playerPlayground = pd.read_json(path+ "/allplayersFormatted.json")
    
    playerPlayground = playerPlayground.rename(columns= {
                        "player-name": "Player",
                        "Team" : "Team",
                        "Age" : "Age",
                        "Pos 1" : "Eligble Position 1",
                        "Pos 2" : "Eligble Position 2",
                        "Pos 3" : "Eligble Position 3",
                        "FP-AVG" : "Fantasy Points Per Game",
                        "FP-TOTAL" : "Overall Fantasy Points Scored",
                        "GP" : "Games Played",
                        "MPG" : "Minutes Per Game",
                        "PPG" : "Points Per Game",
                        "RPG" : "Rebounds Per Game",
                        "APG" : "Assists Per Game",
                        "3PMPG" : "Made 3s Per Game",
                        "OREBPG" : "Offensive Rebounds Per Game",
                        "DREBPG" : "Defensive Rebounds Per Game",
                        "BPG" : "Blocks Per Game",
                        "SPG" : "Steals Per Game",
                        "TPG" : "Turnovers Per Game",
                        "PFPG" : "Personal Fouls Per Game"
                        })

    playerPlayground = playerPlayground.drop(columns= [
                                "sleeper-player-id",
                                "TFPG", 
                                "DD2PG", 
                                "TD3PG",
                                "40+PPG",
                                "50+PPG",
                                "15+APG",
                                "20+RPG",
                                "bdl-player-id",
                                "nba-api-pID"
                                ])

    playerPlayground = playerPlayground.set_index("Player")

    playerPlayground = playerPlayground.dropna(subset=['Fantasy Points Per Game'])

    #PG = 3
    #SG = 3.1
    #SF = 3.3
    #PF = 3.55
    #C = 3.5

    playerPlayground.insert(loc = 5,
            column = 'Position Rating',
            value = 0)

    for i in playerPlayground.index:
        if (
            playerPlayground['Eligble Position 1'][i] == 'PG' or
            playerPlayground['Eligble Position 2'][i] == 'PG' or
            playerPlayground['Eligble Position 3'][i] == 'PG' 
        ):
            playerPlayground['Position Rating'][i] += 4 * 1.19
        if (
            playerPlayground['Eligble Position 1'][i] == 'SG' or
            playerPlayground['Eligble Position 2'][i] == 'SG' or
            playerPlayground['Eligble Position 3'][i] == 'SG' 
        ):
            playerPlayground['Position Rating'][i] += 4 * 1.3
        if (
            playerPlayground['Eligble Position 1'][i] == 'SF' or
            playerPlayground['Eligble Position 2'][i] == 'SF' or
            playerPlayground['Eligble Position 3'][i] == 'SF' 
        ):
            playerPlayground['Position Rating'][i] += 4 * 1.45
        if (
            playerPlayground['Eligble Position 1'][i] == 'PF' or
            playerPlayground['Eligble Position 2'][i] == 'PF' or
            playerPlayground['Eligble Position 3'][i] == 'PF' 
        ):
            playerPlayground['Position Rating'][i] += 4 * 1.49
        if (
            playerPlayground['Eligble Position 1'][i] == 'C' or
            playerPlayground['Eligble Position 2'][i] == 'C' or
            playerPlayground['Eligble Position 3'][i] == 'C' 
        ):
            playerPlayground['Position Rating'][i] += 3 * 1.53

    for column in format_playerPlayground:
        if (
            column == 'Position Rating' or
            column == 'Overall Fantasy Points Scored'
            ):
            playerPlayground[column] = playerPlayground[column].map('{:.2f}'.format)
        elif column == 'Games Played':
            playerPlayground[column] = playerPlayground[column].map('{:.0f}'.format)
        else:
            playerPlayground[column] = playerPlayground[column].map('{:.1f}'.format)

    conversion = {
            "Fantasy Points Per Game" : float,
            'Position Rating' : float,
            'Games Played' : int,
            "Overall Fantasy Points Scored" : float,
            "Points Per Game" : float,
            "Rebounds Per Game" : float,
            "Assists Per Game" : float,
            "Made 3s Per Game" : float,
            "Offensive Rebounds Per Game" : float,
            "Defensive Rebounds Per Game" : float,
            "Blocks Per Game" : float,
            "Steals Per Game" : float,
            "Turnovers Per Game" : float,
            "Personal Fouls Per Game" : float
    }
    
    playerPlayground = playerPlayground.astype(conversion)
    
    playerPlayground.to_pickle(dfPP_filePath)
    
    print("created and pickled " + dfPP_fileName + ".pkl ✓✓✓")
