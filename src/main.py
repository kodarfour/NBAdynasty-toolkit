from methods import *
from backups import *
from sleeper_wrapper import League, User, Stats, Players, Drafts
import json

leagueID = '851103743612141568' #input("Enter Sleeper League ID: ")

# NOTE remove comment for input method to assign a custom path 
# path = input("Enter path to be created/targeted to store backups: ")

# NOTE comment out/delete line below in order for custom path to be assigned
path = "/mnt/c/Users/kodar/Documents/CS-Work/NBAdynasty-toolkit/src/backups"

league = League(leagueID)
drafts = Drafts(leagueID)
players = Players()
stats = Stats()
create_backups_dir(path)

backup_allPlayersFile() 


try: #try to assingn/create backups
    if not check_leagueID(leagueID):
        backup_leagueID(leagueID)

    if check_rostersfile():
        allRosters = set_rostersfile()
    else:
        allRosters = league.get_rosters()
        backup_rostersfile(allRosters)
        
    if check_usersfile():
        allUsers = set_usersfile()
    else:
        allUsers = league.get_users()  
        backup_usersfile(allUsers)

    if check_standingsfile():
        standingsData = set_standingsfile()
    else:
        standingsData = league.get_standings(allRosters, allUsers)
        backup_standingsfile(standingsData)
        
    for i in range(1,18): #cycles through every week (1-17)
        if check_matchupsfile(i):
            print("week" + str(i) + " matchup file already exists ✓✓✓")
        else:
            this_weeks_matchup = league.get_matchups(i)
            backup_matchupsfile(this_weeks_matchup,i)
except:
    print("Couldnt back up or find specified files")
    
set_total_values(standingsData, allRosters, allUsers, path, leagueID)
    
    