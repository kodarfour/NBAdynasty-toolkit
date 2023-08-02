from seasonTotal_methods import *
from backups import *
from sleeper_wrapper import League, User, Stats, Players, Drafts
import json

leagueID = input("Enter Sleeper League ID: ")
league = League(leagueID)
drafts = Drafts(leagueID)
players = Players()
stats = Stats()
create_backups_dir()

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
        print("Couldnt back up files")

    keys = ['win%', 
            'total FP', 
            'total opposing FP', 
            'total max FP', 
            'total game pick eff', 
            'power rank', 
            'avg pd'
            ]
    categories = ["Record / Win Percentage / Seeding",
                "Total Scored FP",
                "Total Opposing FP",
                "Total Max FP",
                "Game Pick Efficiency",
                "Power Ranking",
                "Average Point Differential"
                ]
    order = ["an ascending", "a descending", "(low to high)", "(high to low)"]

    set_total_values(standingsData, allRosters, allUsers)

    test = True
    print("\nLeague Standings Menu (TOTAL SEASON) OPENED...\n")

    while(test): #while loop that goes through Total Season Menu
        while(True):
            try:
                print("Read and follow instructions below carefully.")
                for j in range(2):
                    print("Input \"" + str(j) + "\" if you want to sort in "+ order[j] + ". " + order[j+2])
                orderNum = int(input("Enter here: "))
                if orderNum != 1 and orderNum != 0:
                    print("Force error" + 1)
            except:
                print("\nERROR: Invalid input! Must be an integer, and must be \"0\" or \"1\". Try again.\n")
                continue
            finally:
                if orderNum == 0:
                    order_statement = "\nHere are league standings sorted in an ascending order "
                    order_warning = " REMEMBER: you selected ascending order (low to high)."
                elif orderNum == 1:
                    order_statement = "\nHere are league standings sorted in a descending order "
                    order_warning = " REMEMBER: you selected descending order (high to low)."
            break
        
        print("")

        while(True):
            try:
                print("Follow instructions below carefully." + order_warning)
                for i in range(len(categories)):
                    print("Input \""+ str(i) +"\" if you want to sort the \"" + categories[i]+ "\" category.")
                categoryNum = int(input("Enter here: "))
                
                if not (categoryNum in range(7)):
                    print("Force error" + 1)
            except:
                print("\nERROR: Invalid input! Must be an integer, and must be one of \"0\" through \"6\". Try again.\n")
                continue
            else:
                category_statement = "using the \"" + categories[categoryNum] +"\"\n"
            break
        
        print(order_statement + category_statement + " category:")
        sort_by_category(orderNum, keys[categoryNum]) #should sort total max fp, in descending order
        display_standings()
        print("")

        while(True):
            try:
                tryAgain = input("Do you want to display standings again? \"Yes\" or \"No\": ")
                if (tryAgain != "Yes") and (tryAgain != "No"):
                    print("Force an Error" + 1)
            except:    
                print("\nERROR: Invalid input, make sure to match capitilization. Input must be \"Yes\" or \"No\" exactly. Try Again.\n")
                continue
            else:
                if tryAgain.rstrip(" ").lstrip(" ") == "Yes":
                    print("")
                    pass
                else:
                    print("\nLeague Standings Menu CLOSED (TOTAL SEASON)...\n")
                    test = False
            break


