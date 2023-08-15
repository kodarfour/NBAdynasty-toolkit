# NBA Dynasty Recapper  
A web app to recap the basketBalls 2022-2023 Fantasy Dynasty NBA season from the Sleeper APP (Game Pick Format)

This web app was created in order to fix my comissioner errors during the playoffs of the my fantasy league. I accidentally erased all players and scoring data when messing with comissioner tools.

# Dependencies:
 - [NBA API Endpoints Library](https://pypi.org/project/nba-api/)
 - [BallDontLie API](https://www.balldontlie.io/home.html#introduction) 
    - Nothing to install, just info on its endpoints
 - [Sleeper-API-Wrapper](https://github.com/dtsong/sleeper-api-wrapper#install)
 - [Sleeper API](https://docs.sleeper.com/)
    - Nothing to install, just info on its endpoints
 - [pandas](https://pandas.pydata.org/docs/getting_started/install.html#installing-pandas)
 - [dtale](https://pypi.org/project/dtale/)
 - [Python 3.7+](https://www.python.org/downloads/)
 - [requests](https://pypi.org/project/requests/)
 - [flask](https://flask.palletsprojects.com/en/2.3.x/installation/#install-flask)

# Instructions:
**PRE-REQ:** Install Dependencies and set up virtualenv for Flask App 
    - [Terminal Instructions](https://www.twilio.com/docs/usage/tutorials/how-to-set-up-your-python-and-flask-development-environment)
    - [VS Code Instructions](https://code.visualstudio.com/docs/python/environments)
    - [WSL and VS Code Instructions](https://thecodeblogger.com/2020/09/24/wsl-setup-vs-code-for-python-development/)

**FIRST:** Run setup.py 
 - Make sure to note:
    - Assign path variable to accurate directory
    - Methods backup_allPlayersFile() and set_total_values() take a very long time to finish (if you delete allplayerFormatted.json and tMyLeagueData-851103743612141568.json files)vbecause it relies on the NBA API and BallDontLie API and it requests alot of information. Therefore, it uses sleep timers to not cause API Call throttling. The process can take hours...Make sure to not lose provided files in .../src/backups as it speeds the setup.py progam substancially by not having to call any APIs!!!!
    - If you decide to run those by your self note problemPlayers_fixedPositions.txt file It contains a copy of the allPlayersFormatted.json information but with fixed data entry for the following:
        - players with periods in thier name (ex: P.J. Tucker) as Sleeper/BallDontLie/NBA API have names saved with and without the periods, causing failures in api calls. (program will still run but with missing info)
        - players with Jr. in their name (ex: Jaren Jacksn Jr) as Sleepr API doesnt include it in their player info
        - players with a number in their name (ex: Trey Murphy III) as Sleepr API doesnt include it in their player info
        - corrected position orders for players as Sleeper lists them randomly but the first position is essential when using the player playground in the app as it represents thier main position and can be crucial in determining which position has the best fantasy scorers.
    - It is essential that you delete the text from allPlayerFormatted.json and replace it with the text in problemPlayers_fixedPositions.txt inorder for weekly values to work properly and for the playerplayground page to display all eligble players (it excludes all players who didnt log stats in the nba 2022-2023 season) 
    - LASTLY, As the years go on and players retire, some players may become inacitve which will break the use of the  program, so be sure to use provided allplayerFormatted.json and tMyLeagueData-851103743612141568.json files if problems arise
    - Do not change order of methods called, the program will break.
    
**SECOND:** Run app.py
 - Make sure to note:
    - Assign path variable to accurate directory
    - Assign variables:
        - dtale_PORT to whatever port of your preference (cannot be same as app_PORT),
        - app_PORT to whatever port of your preference (cannot be same as dtale_PORT)
        - HOST set to whatever host of your preference
    
