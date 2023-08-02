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

#LEAGUEIDFILE (check, backup)

def check_leagueID(leagueID):
    global leagueID_fileName
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
    r_fileName = "rostersfile.json"
    obj = Path(path+"/"+r_fileName)
    return obj.exists()
    

def backup_rostersfile(data):
    r_fileName = "rostersfile.json"
    r_filePath = os.path.join(path, r_fileName)
    newJSON = json.dumps(data, indent = 4, sort_keys= True)
    if os.path.exists(path):
        print("creating rosters file...")
        with open(r_filePath, "w") as f:
            f.write(newJSON)
        print("created " + r_fileName + " ✓✓✓")

def set_rostersfile():
    r_fileName = "rostersfile.json"
    r_filePath = os.path.join(path, r_fileName)
    print("assigning rostersfile data...")
    with open(r_filePath) as newJSON:
        result = json.load(newJSON)
    print("assigned " + r_fileName + " ✓✓✓")
    return result
    
#USERSFILE (check, backup, set)

def check_usersfile():
    global u_fileName
    u_fileName = "usersfile.json"
    obj = Path(path+"/"+u_fileName)
    return obj.exists()

def backup_usersfile(data):
    u_fileName = "usersfile.json"
    u_filePath = os.path.join(path, u_fileName)
    newJSON = json.dumps(data,indent = 4, sort_keys= True)
    if os.path.exists(path):
        print("creating users file...")
        with open(u_filePath, "w") as f:
            f.write(newJSON)
        print("created " + u_fileName + " ✓✓✓")

def set_usersfile():
    u_fileName = "usersfile.json"
    u_filePath = os.path.join(path, u_fileName)
    print("assigning usersfile data...")
    with open(u_filePath) as newJSON:
        result = json.load(newJSON)
    print("assigned " + u_fileName + " ✓✓✓")
    return result

#STANDINGSFILE (check, backup, set)

def check_standingsfile():
    global s_fileName
    s_fileName = "standingsfile.json"
    obj = Path(path+"/"+s_fileName)
    return obj.exists()

def backup_standingsfile(data):
    s_fileName = "standingsfile.json"
    s_filePath = os.path.join(path, s_fileName)
    newJSON = json.dumps(data,indent = 4, sort_keys= True)
    if os.path.exists(path):
        print("creating standings file...")
        with open(s_filePath, "w") as f:
            f.write(newJSON)
        print("created " + s_fileName + " ✓✓✓")

def set_standingsfile():
    s_fileName = "standingsfile.json"
    s_filePath = os.path.join(path, s_fileName)
    print("assigning standingsfile data...")
    with open(s_filePath) as newJSON:
        result = json.load(newJSON)
    print("assigned " + s_fileName + " ✓✓✓")
    return result

def check_tMyLeague():
    global tMyLeague_fileName
    tMyLeague_fileName = "tMyLeagueData.json"
    obj = Path(path+"/"+tMyLeague_fileName)
    return obj.exists()

def backup_tMyLeague(data): #t is for total
    tMyLeague_fileName = "tMyLeagueData.json"
    tMyLeague_filePath = os.path.join(path, tMyLeague_fileName)
    newJSON = json.dumps(data,indent = 4, sort_keys= True)
    if os.path.exists(path):
        with open(tMyLeague_filePath, "w") as f:
            f.write(newJSON)

def set_tMyLeague():
    tMyLeague_fileName = "tMyLeagueData.json"
    tMyLeague_filePath = os.path.join(path, tMyLeague_fileName)
    with open(tMyLeague_filePath) as newJSON:
        return  json.load(newJSON)