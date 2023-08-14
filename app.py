from flask import *
from dtale.global_state import *
import dtale
import pandas as pd

leagueID = '851103743612141568'

path = "/mnt/c/Users/kodar/Documents/CS-Work/NBAdynasty-toolkit/src/backups"

dfLS_fileName = "df_leagueStandings-" + leagueID
dfLS_filePath = path + "/" + dfLS_fileName + ".pkl"
df_leagueStandings = pd.read_pickle(dfLS_filePath)

dfPP_fileName = "df_playerPlayground-" + leagueID
dfPP_filePath = path + "/" + dfPP_fileName + ".pkl"
df_playerPlayground = pd.read_pickle(dfPP_filePath)

app = Flask(__name__)
if __name__ == '__main__':
    @app.route('/')
    def home():
        return redirect('index')
    
    @app.route('/standings')
    def standings():
        cleanup()
        dtale.show(
            df_leagueStandings, 
            host='localhost', 
            port = 4000, 
            subprocess = True, 
            force = True, 
            hide_header_editor= True
            )
        return render_template('standings.html')

    @app.route('/playground')
    def playground():
        cleanup()
        dtale.show(
            df_playerPlayground, 
            host='localhost', 
            port = 4000, 
            subprocess = True, 
            force = True, hide_header_editor= True
            )
        return render_template('playground.html')
        
    @app.route('/index')
    def index():
        return render_template('index.html')

    app.run() 
    
