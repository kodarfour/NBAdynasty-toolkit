import os
from pathlib import Path
from sleeper_wrapper import League, User, Stats, Players, Drafts
import time, json, requests
from seasonTotal_methods import *

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
    data =  requests.get('https://api.sleeper.app/v1/players/nba')
    print(data)
    if data.status_code == 200:
        print("requesting all player data from Sleeper API...")
        rawJSON = data.json()
        playerList = []

        for k in rawJSON.keys():
            innerDict = rawJSON[k]
            if (innerDict["active"] and innerDict["team"] is not None): #if player IS active AND IS on a team
                try:
                    test_if_playerID_is_Integer = int(k) #if ID is an integer, go as planned
                    playerDict = {
                        "player-id": None,
                        "player-name": None,
                        "Team" : None,
                        "Age" : None,
                        "Pos 1" : None,
                        "Pos 2" : None,
                        "Pos 3" : None,
                        "Pos 4" : None,
                        "PTS" : None,
                        "REB" : None,
                        "AST" : None,
                        "OREB" : None,
                        "DREB" : None,
                        "BLK" : None,
                        "STL" : None,
                        "TOV" : None,
                        "FPS" : None
                    }
                    
                    playerDict["player-id"] = k
                    playerDict["Team"] = innerDict['team']
                    playerDict["Age"] = innerDict['age']
                    playerDict["player-name"] = innerDict['full_name']

                    for i in range(len(innerDict["fantasy_positions"])): #iterates through all position
                        try:
                            posNum = str((i+1))
                            playerDict["Pos " + posNum] = innerDict['fantasy_positions'][i] # sets fantasy position at playerDict key
                        except: 
                            break # if no position at index it stops running
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
        print("ERROR: File creation FAILED!")

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