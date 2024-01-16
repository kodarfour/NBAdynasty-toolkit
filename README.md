# Dynasty Recapper
A web app to recap the "basketBalls" 2022-2023 Fantasy Dynasty NBA season from the Sleeper APP (Game Pick Format)

Created in order to fix my comissioner errors during the playoffs of the my fantasy league. I accidentally erased all players and scoring data when tinkering with comissioner tools.

# Dependencies:
 - [nba_api](https://pypi.org/project/nba-api/) 
   - [API Endpoints Information](https://github.com/swar/nba_api/tree/master/docs/nba_api/stats/endpoints)
 - BallDontLie API
    - [API Endpoints Information](https://www.balldontlie.io/home.html#introduction)
 - Sleeper API
    - [API Endpoints Information](https://docs.sleeper.com/)
 - [Sleeper-API-Wrapper](https://github.com/dtsong/sleeper-api-wrapper#install)
 - [pandas](https://pandas.pydata.org/docs/getting_started/install.html#installing-pandas)
 - [dtale](https://pypi.org/project/dtale/)
 - [Python 3.7+](https://www.python.org/downloads/)
 - [requests](https://pypi.org/project/requests/)
 - [flask](https://flask.palletsprojects.com/en/2.3.x/installation/#install-flask)

# Instructions:
**<em>FIRST: Install Dependencies and set up virtualenv for Flask</em>**
To install all required Python packages, navigate to the appropriate directory and run:
> pip install -r requirements.txt
 - [Terminal Instructions](https://www.twilio.com/docs/usage/tutorials/how-to-set-up-your-python-and-flask-development-environment)
 - [VS Code Instructions](https://code.visualstudio.com/docs/python/environments)
 - [WSL and VS Code Instructions](https://thecodeblogger.com/2020/09/24/wsl-setup-vs-code-for-python-development/)

**<em>SECOND: Run setup.py</em>**
 - Make sure to note <ins>BEFORE</ins> running:
    - Assign <code>path</code>  variable to accurate directory
    - Methods <code>backup_allPlayersFile()</code> and <code>set_total_values()</code> take a very long time to finish (if you delete <code>allplayerFormatted.json</code> and <code>tMyLeagueData-851103743612141568.json</code> files)  because it relies on the NBA API and BallDontLie API and it requests alot of information. Therefore, it uses sleep timers to not cause API Call throttling. The process can take hours... Make sure to not lose provided files in <code>.../src/backups</code> as it decreases the <code>setup.py</code> progam's runtime substancially by not having to call any APIs!!!!
    - If you decide to run those by your self note <code>problemPlayers_fixedPositions.txt</code> file It contains a copy of the <code>allPlayersFormatted.json</code> information but with fixed data entry for the following:
        - players with periods in thier name (ex: P.J. Tucker) as Sleeper/BallDontLie/NBA API have names saved with and without the periods, causing failures in api calls. (program will still run but with missing info)
        - players with Jr. in their name (ex: Jaren Jacksn Jr) as Sleepr API doesnt include it in their player info
        - players with a number in their name (ex: Trey Murphy III) as Sleepr API doesnt include it in their player info
        - corrected position orders for players as Sleeper stores them randomly but the first position is essential when using the player playground in the app as it represents thier main position and can be crucial in determining which position has the best fantasy scorers.
    - If you call <code>backup_allPlayersFile()</code> (whether it be to test the execution and etc.), it is essential that you delete the text from <code>allPlayerFormatted.json</code> and replace it with the text in <code>problemPlayers_fixedPositions.txt</code> inorder for weekly values to work properly and for the playerplayground page to display all eligble players (it excludes all players who didnt log stats in the nba 2022-2023 season) 
    - LASTLY, As the years go on and players retire, some players may become inacitve which will break the use of the  program, so be sure to use provided <code>allplayerFormatted.json</code> and <code>tMyLeagueData-851103743612141568.json</code> files if problems arise
    - Do not change order of methods called, the data will not be accurate or the program fail.
    
**<em>THIRD: Run app.py</em>**
 - Make sure to note <ins>BEFORE</ins> running:
    - Assign <code>path</code>  variable to accurate directory
    - Assign variables:
        - <code>dtale_PORT</code>  to whatever port of your preference (cannot be same as <code>app_PORT</code> )
        - <code>app_PORT</code>  to whatever port of your preference (cannot be same as <code>dtale_PORT</code> )
        - <code>HOST</code>  set to whatever host of your preference

**<em>FINALLY: Explore the Web App!</em>**

# Demo:

Watch video below for a demo:

[![Watch the video](https://img.youtube.com/vi/WF-bI5ZELvc/maxresdefault.jpg)](https://www.youtube.com/watch?v=WF-bI5ZELvc)