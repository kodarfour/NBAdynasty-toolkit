from seasonTotal_methods import *
from sleeper_wrapper import League, User, Stats, Players, Drafts
"""
League ID: 851103743612141568
"""
import json

leagueID = input("Enter Sleeper League ID: ")
league = League(leagueID)
drafts = Drafts(leagueID)
players = Players()
stats = Stats()

allRosters = league.get_rosters()  
allUsers = league.get_users()  
standingsData = league.get_standings(allRosters, allUsers)

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
set_total_values(standingsData, allRosters, allUsers)

test = True
print("League Standings Menu (TOTAL SEASON) OPENED...\n")

while(test):
    while(True):
        try:
            print("Read and follow instructions below carefully.")
            print("Input \"0\" if you want to sort in an ascending order. (low to high)")
            print("Input \"1\" if you want to sort in a descending order. (high to low)")
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
            print("Input \"0\" if you want to sort the \"Record / Win Percentage / Seeding\" category.")
            print("Input \"1\" if you want to sort the \"Total Scored FP\" category.")
            print("Input \"2\" if you want to sort the \"Total Opposing FP\" category.")
            print("Input \"3\" if you want to sort the \"Total Max FP\" category.")
            print("Input \"4\" if you want to sort the \"Game Pick Efficiency\" category.")
            print("Input \"5\" if you want to sort the \"Power Ranking\" category.")
            print("Input \"6\" if you want to sort the \"Average Point Differential\" category.")
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
                print("League Standings Menu CLOSED (TOTAL SEASON)...")
                test = False
        break


