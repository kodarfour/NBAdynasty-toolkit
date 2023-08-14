from methods import *
from backups import *
from sleeper_wrapper import League, Players
import pandas  as pd
# from pandasgui import show
import dtale

leagueID = '851103743612141568' #input("Enter Sleeper League ID: ")

# NOTE remove comment for input method to assign a custom path 
# path = input("Enter path to be created/targeted to store backups: ")

# NOTE comment out/delete line below in order for custom path to be assigned
path = "/mnt/c/Users/kodar/Documents/CS-Work/NBAdynasty-toolkit/src/backups"

league = League(leagueID)
players = Players()
create_backups_dir(path)

if check_allPlayersFile():
    print("allplayers file already exists ✓✓✓")
else:
    backup_allPlayersFile() 


try: #try to assingn/create backups
    if check_leagueID(leagueID):
        print("league id file already exists ✓✓✓")
    else:
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

dfLS_fileName = "df_leagueStandings-" + leagueID
dfLS_filePath = path + "/" + dfLS_fileName + ".pkl"

if check_df_leagueStandings():
    print("unpickling league standings dataframe ...")
    df_leagueStandings = pd.read_pickle(dfLS_filePath)
    print("assigned " + dfLS_fileName + ".pkl ✓✓✓")
else:
    backup_df_leagueStandings()
    df_leagueStandings = pd.read_pickle(dfLS_filePath)

dfPP_fileName = "df_playerPlayground-" + leagueID
dfPP_filePath = path + "/" + dfPP_fileName + ".pkl"

if check_df_playerPlayground():
    print("unpickling player playground dataframe ...")
    df_playerPlayground = pd.read_pickle(dfPP_filePath)
    print("assigned " + dfPP_fileName + ".pkl ✓✓✓")
else:
    backup_df_playerPlayground()
    df_playerPlayground = pd.read_pickle(dfPP_filePath)
df = dtale.show(df_playerPlayground, host='localhost', subprocess = False)
print(df._main_url)
