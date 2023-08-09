import os
from pathlib import Path
from sleeper_wrapper import League, User, Stats, Players, Drafts
import time, json, requests
from methods import *
from flask import *
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players


#creat backups director
def create_backups_dir(p):
    global path
    path = p 
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)
            raise

#player files !!FETCH ONCE PER DAY!! (check, backup)

def check_allPlayersFile():
    global ap_fileName
    pass

def backup_allPlayersFile():
    ap_fileName = "allplayersFormatted.json"
    ap_filePath = os.path.join(path, ap_fileName)
    data = requests.get('https://api.sleeper.app/v1/players/nba')
    print(data)
    if data.status_code == 200:
        
        with open(path+"/"+"allplayersFailLog.txt","w") as f:
            f.write("LOG:"+"\n")
            f.close()
        
        print("requesting all player data from Sleeper API...")
        rawJSON = data.json()
        playerList = []

        for k in rawJSON.keys():
            innerDict = rawJSON[k]
            if (innerDict["active"] and innerDict["team"] is not None): #if player IS active AND IS on a team
                playerDict = {
                    "sleeper-player-id": None,
                    "player-name": None,
                    "Team" : None,
                    "Age" : None,
                    "Pos 1" : None,
                    "Pos 2" : None,
                    "Pos 3" : None,
                    "Pos 4" : None,
                    "FPPG" : None,
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
                    "FFPG" : None,
                    "DDPG" : None,
                    "TDPG" : None,
                    "40+PPG": None,
                    "50+PPG": None,
                    "15+APG": None,
                    "20+RPG" : None,
                    "bdl-player-id" : None,
                    "nba-api-pID" : None
                }
                try:
                    test_if_playerID_is_Integer = int(k) #if ID is an integer, go as planned
                    playerDict["sleeper-player-id"] = k
                    playerDict["Team"] = innerDict['team']
                    playerDict["Age"] = innerDict['age']
                    playerDict["player-name"] = innerDict['full_name']
                    
                        
                    for i in range(len(innerDict["fantasy_positions"])): #iterates through all position
                        try:
                            posNum = str((i+1))
                            playerDict["Pos " + posNum] = innerDict['fantasy_positions'][i] # sets fantasy position at playerDict key
                        except: 
                            break # if no position at index it stops running
                    
                    try:
                        get_bdl_playerData = requests.get("https://www.balldontlie.io/api/v1/players/?search=" + playerDict["player-name"])
                        if get_bdl_playerData.status_code == 200:
                            bdl_playerData = get_bdl_playerData.json()
                            bdl_playerID = bdl_playerData["data"][0]["id"]
                        time.sleep(1.3)
                        #gets player averages
                        get_bdl_playerAverages = requests.get("https://www.balldontlie.io/api/v1/season_averages?season=2022&player_ids[]="+str(bdl_playerID))
                        if get_bdl_playerAverages.status_code == 200:
                            averagesData = get_bdl_playerAverages.json()
                        # averagesData = get_bdl_playerAverages(playerDict["player-name"])
                        onlyStats = averagesData["data"][0]
                        
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
                        print("Success! "+ playerDict["player-name"])
                        try:
                            playerDict["nba-api-pID"] = players.find_players_by_full_name(playerDict["player-name"])[0]['id']
                            
                            playerDict["40+PPG"] = 0
                            playerDict["50+PPG"] = 0
                            playerDict["15+APG"] = 0
                            playerDict["20+RPG"] = 0
                            playerDict["DDPG"] = 0
                            playerDict["TDPG"] = 0
                            
                            gamelog_thisPlayer = playergamelog.PlayerGameLog(player_id=playerDict["nba-api-pID"], season = '2022').get_dict()
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
                                    playerDict["DDPG"] += 1
                                
                                #triple doubles
                                # pts >= 10
                                # rebs >= 10
                                # asts >= 10
                                # stls >= 10
                                # blks >= 10
                                
                                if(
                                    (pts >= 10 and rebs >= 10 and asts >= 10) or
                                    (pts >= 10 and rebs >= 10 and stls >= 10) or
                                    (pts >= 10 and rebs >= 10 and blks >= 10) or
                                    (rebs >= 10 and asts >= 10 and stls >= 10) or
                                    (rebs >= 10 and asts >= 10 and blks >= 10) or
                                    (asts >= 10 and stls >= 10 and blks >= 10) 
                                ):
                                    playerDict["TDPG"] += 1
                            
                            playerDict["40+PPG"] /= playerDict["GP"]
                            playerDict["50+PPG"] /= playerDict["GP"]
                            playerDict["15+APG"] /= playerDict["GP"]
                            playerDict["20+RPG"] /= playerDict["GP"]
                            playerDict["DDPG"] /= playerDict["GP"]
                            playerDict["TDPG"] /= playerDict["GP"]

                            fp_average = (
                                (playerDict["PPG"]) +
                                (playerDict["RPG"] * 1.15) +
                                (playerDict["APG"] * 1.7)  +
                                (playerDict["SPG"] * 2)  +
                                (playerDict["BPG"] * 2.7)  +
                                (playerDict["TPG"] * -1)  +
                                (playerDict["DDPG"] * 2)  +
                                (playerDict["TDPG"] * 3.5)  +
                                (playerDict["PFPG"] * -.15)  +
                                (playerDict["3PMPG"] * 1.7)  +
                                (playerDict["OREBPG"] * 0.5)  +
                                (playerDict["40+PPG"] * 3)  +
                                (playerDict["50+PPG"] * 5)  +
                                (playerDict["15+APG"] * 4)  +
                                (playerDict["20+RPG"] * 5)  
                            )
                            
                            playerDict["FPPG"] = fp_average
                            
                            print("NBA API PLAYER ID SUCCESS! " + playerDict["player-name"])

                        except:
                            with open(path+"/"+"allplayersFailLog.txt","a") as f:
                                f.write("NBA API PLAYER ID FAIL! " + playerDict["player-name"]+"\n")
                                f.close()
                            print("NBA API PLAYER ID FAIL! " + playerDict["player-name"])
                        
                    except:
                        with open(path+"/"+"allplayersFailLog.txt","a") as f:
                                f.write("ERROR: Player season averages data retrieval failed! " + playerDict["player-name"]+"\n")
                                f.close()
                        print("ERROR: Player season averages data retrieval failed! " + playerDict["player-name"])
                    finally:
                        playerList.append(playerDict)
                except: # if not an integers go to next dict
                    continue
        
        print("recieved all player data from Sleeper API ✓✓✓")
        newJSON = json.dumps(playerList ,indent = 2) # creates json info
        
        if os.path.exists (path):
            print("creating/updating all players file...")
            with open(ap_filePath, "w") as f:
                f.write(newJSON)
            print("created/updated " + ap_fileName + " ✓✓✓")
    else:
        print("ERROR: Invalid Response Code (not 200)!!!")

#LEAGUEIDFILE (check, backup)

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

#ROSTERSFILE (check, backup, set)

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
    
#USERSFILE (check, backup, set)

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

#STANDINGSFILE (check, backup, set)

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

#MATCHUPSFILE (check, backup, set)

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

#TMYLEAGUEDATA (check, backup, set)

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