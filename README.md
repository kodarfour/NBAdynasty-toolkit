# NBAdynasty-toolkit
An app to help Dynasty NBA players on the Sleeper APP (Game Pick Format)

**Priority Features:**

- Weekly Rankings:
  - Standings (use api call)
  - Seeding Record (Win-loss) and Win Rate [(2 × Wins + Ties) / (2 × Total Games Played)]
    - Include Clinches and Playoff Elimination
  - Total FP( use api call)
  - Opposing FP(use api call)
  - Max FP(use api call) 
  - Game pick efficiency (Total FP / Max FP)
  - AVG Point Differential [(Average Total FP) - (Average Opposing FP)] 
    - High APD = Consistently Dominating Matchups, implies super efficient game picks or very powerful fantasy output
    - Low APD = Consistently Losing or winning in very close Margins, might want to make roster changes or become more efficient
  - Power Rankings [(Points Scored x2) + (Points Scored \* Winning %) + (Points Scored \* Winning %)]
- Award Tracker
  - Best Team
  - Worst Team
  - Most Efficient
  - Least Efficient
  - Highest FP in Loss
  - Lowest FP in a Win
- Make Sure you can sort High to Low for each category
- Highlight the highest and lowest team for each category
- Draft Pick Standings Tracker: 
  - First Round: Lottery (10/9/8 seed) → 1st seed
    - 10th → 48% | 9th → 36% | 8th → 16%
    - By default have lottery picks in order by standing but have a setting that allows you to simulate lottery at end of season and updating accordingly
  - Second Round: Lowest Max PF → Highest Max PF
  - Third Round: Snakes off the Second Round

**Future Features:**

- Playoff Odds Calculator using montecarlo simulations
- Roster Evaluation
  - Use Player positions and average Fantasy points to rate diversity and depth
  - Display Positional Need, Strongest / Weakest Position
  - Display Average Age of roster
- Schedule Comparison 
  - <https://drive.google.com/drive/folders/1qCTBulFWSgHz3thLqDe5DcZ6AIJWkZQ_?usp=sharing> FFHUB charts to recreate
- Trade Calculator using current value of draft assets and Dynasty Rankings Online
- Excel Integration
- Website/GUI Interface
- Team Depth Charts (creates list for each position in order of average fantasy points)

**Needed Technology / Knowledge:**

- Python 3
- API Calls 
  - Sleeper API = https://docs.sleeper.com/
  - <https://realpython.com/api-integration-in-python/> 
  - <https://www.dataquest.io/blog/python-api-tutorial/>
  - <https://www.educative.io/answers/how-to-make-api-calls-in-python>

- Django/ React/ Javascript/ HTML CSS3/ Node.js
  - https://www.cronj.com/blog/integrating-python-with-nodejs-and-react-a-powerful-combination-for-web-developmen/
  - <https://www.fullstackpython.com/react.html>
  - <https://blog.logrocket.com/python-developers-guide-react/>
  - <https://www.w3schools.com/js/>
  - <https://www.w3schools.com/html/default.asp>
  - <https://www.w3schools.com/css/default.asp>

- Github
  - <https://www.freecodecamp.org/news/how-to-use-git-and-github-in-a-team-like-a-pro/>
  - <https://www.digitalcrafts.com/blog/learn-how-start-new-group-project-github>
  - <https://devmountain.com/blog/what-is-github-and-how-do-you-use-it/>
  - PyCharm Integration -  <https://www.jetbrains.com/help/pycharm/set-up-a-git-repository.html>
  - VS Code Integration - <https://code.visualstudio.com/docs/sourcecontrol/intro-to-git>
  - WSL Terminal Git Use - <https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git>
  - Windows Terminal Git Use -  https://linuxhint.com/add-git-bash-windows-terminal/

- Equations/Formulas
  - Playoff Odds 
    - <https://drive.google.com/drive/folders/1qCTBulFWSgHz3thLqDe5DcZ6AIJWkZQ_?usp=sharing> Medium Article PDF alternatives
    - <https://towardsdatascience.com/how-to-create-a-monte-carlo-simulation-using-python-c24634a0978a>)
    - <https://medium.com/geekculture/how-to-calculate-probability-versus-odds-using-python-53e5e73cbde2>
    - https://www.massivereportdata.com/blog/2017/10/15/how-im-simulating-playoff-odds/
