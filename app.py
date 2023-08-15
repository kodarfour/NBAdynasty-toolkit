from flask import *
from dtale.global_state import *
import dtale
import pandas as pd

leagueID = '851103743612141568'

#NOTE edit path to appropriate directory in your workspace
path = "/mnt/c/Users/kodar/Documents/CS-Work/NBAdynasty-toolkit/src/backups"
#example: .../NBAdynasty-toolkit/src/backups

dfLS_fileName = "df_leagueStandings-" + leagueID
dfLS_filePath = path + "/" + dfLS_fileName + ".pkl"
df_leagueStandings = pd.read_pickle(dfLS_filePath)

dfPP_fileName = "df_playerPlayground-" + leagueID
dfPP_filePath = path + "/" + dfPP_fileName + ".pkl"
df_playerPlayground = pd.read_pickle(dfPP_filePath)

app = Flask(__name__)
if __name__ == '__main__':
    dtale_PORT = 4000 #set to whatever port of your preference (cannot be same as app_PORT)
    app_PORT = 5000 #set to whatever port of your preference (cannot be same as dtale_PORT)
    HOST = 'localhost' #set to whatever host of your preference
    
    @app.route('/')
    def home():
        return redirect('index')
    
    @app.route('/standings')
    def standings():
        cleanup()
        dtale.show( 
            df_leagueStandings, 
            host= HOST, 
            port = dtale_PORT,
            subprocess = True, 
            force = True, 
            hide_header_editor= True
            )
        PORT = str(dtale_PORT)
        return render_template('standings.html', HOST = HOST, PORT = PORT)

    @app.route('/playground')
    def playground():
        cleanup() 
        dtale.show(
            df_playerPlayground, 
            host= HOST, 
            port = dtale_PORT, 
            subprocess = True, 
            force = True, 
            hide_header_editor= True
            )
        PORT = str(dtale_PORT)
        return render_template('playground.html', HOST = HOST, PORT = PORT)
        
    @app.route('/index')
    def index():
        return render_template('index.html')

    app.run(port=app_PORT, host=HOST) 
    
