from flask import *
from dtale.global_state import *
from dtale.views import *
import dtale
from methods import *
from backups import *
from sleeper_wrapper import League, Players
import pandas  as pd
# from pandasgui import show


leagueID = '851103743612141568' #input("Enter Sleeper League ID: ")

# NOTE remove comment for input method to assign a custom path 
# path = input("Enter path to be created/targeted to store backups: ")

# NOTE comment out/delete line below in order for custom path to be assigned
path = "/mnt/c/Users/kodar/Documents/CS-Work/NBAdynasty-toolkit/src/backups"

print("test")

dfLS_fileName = "df_leagueStandings-" + leagueID
dfLS_filePath = path + "/" + dfLS_fileName + ".pkl"



df_leagueStandings = pd.read_pickle(dfLS_filePath)
print("assigned " + dfLS_fileName + ".pkl ✓✓✓")

dfPP_fileName = "df_playerPlayground-" + leagueID
dfPP_filePath = path + "/" + dfPP_fileName + ".pkl"


df_playerPlayground = pd.read_pickle(dfPP_filePath)
print("assigned " + dfPP_fileName + ".pkl ✓✓✓")









app = Flask(__name__)
if __name__ == '__main__':
    @app.route('/')
    def home():
        return redirect('index')

    
    @app.route('/standings')
    def standings():
        cleanup()
        dtale.show(df_leagueStandings, host='localhost', port = 4000, subprocess = True, force = True, hide_header_editor= True)
        return render_template('standings.html')


    #df2 = dtale.show(df_playerPlayground)

    #print(df2._main_url)

    @app.route('/playground')
    def playground():
        cleanup()
        dtale.show(df_playerPlayground, host='localhost', port = 4000, subprocess = True, force = True, hide_header_editor= True)
        #print(df._main_url)
        return render_template('playground.html')
        

    @app.route('/index')
    def index():
        return render_template('index.html')

    app.run() 
    
