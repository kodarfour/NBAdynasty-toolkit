from seasonTotal_methods import *
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

#backup_allPlayersFile()

menu_pick = input("Select Menu (Total, Weekly): ")
if menu_pick == "Total": #activate total league standings menu
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
    except:
        print("Couldnt back up or find specified files")
        
    set_total_values(standingsData, allRosters, allUsers)

elif menu_pick=="Weekly":
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
    except:
        print("Couldnt back up or find specified files")
    