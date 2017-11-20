
import json
import requests
import pandas as pd
import numpy as np

searchTeam = 'DET'

#// Start by searching for team ID // 

url = 'https://statsapi.web.nhl.com/api/v1/teams'

resp = requests.get(url=url)
teamData = json.loads(resp.text)
teamData = teamData['teams'][0:]
teamIndex = pd.DataFrame(np.nan, range(0,31), columns=['ID','TeamName'])

for x in range (0,len(teamData)):
    teamIndex['ID'][x] = teamData[x]['franchiseId']
    teamIndex['TeamName'][x] = teamData[x]['abbreviation']


TeamID = np.flatnonzero(teamIndex['TeamName'] == searchTeam)+1
TeamID = str(TeamID[0])

#// Search for Team Roster IDs // 

url = url+'/'+TeamID+'/roster'

resp = requests.get(url=url)
rosterData = json.loads(resp.text)

roster = rosterData['roster']
rosterIDs = pd.DataFrame(np.nan, range(0,len(roster)), columns=['playerID','playerName','pos'])

for x in range (0,len(roster)):
    rosterIDs['playerID'][x] = roster[x]['person']['id']
    rosterIDs['playerName'][x] = roster[x]['person']['fullName']
    rosterIDs['pos'][x] = roster[x]['position']['code']
    
goalielist = list(rosterIDs['pos'])
numplayers = 0
numgoalies = 0

for x in range(0,len(rosterIDs)):
    if goalielist[x].find("G") == -1:
        numplayers = numplayers+1
    else:
        numgoalies = numgoalies+1
        
        
playerIDs = pd.DataFrame(np.nan, range(0,numplayers), columns=['playerID','playerName','pos'])
goalieIDs = pd.DataFrame(np.nan, range(0,numgoalies), columns=['playerID','playerName','pos'])

p=0
g=0

for x in range(0,len(goalielist)):
    if goalielist[x].find("G") == -1:
        playerIDs['playerID'][p] = roster[x]['person']['id']
        playerIDs['playerName'][p] = roster[x]['person']['fullName']
        playerIDs['pos'][p] = roster[x]['position']['code']
        p = p+1
    else:
        goalieIDs['playerID'][g] = roster[x]['person']['id']
        goalieIDs['playerName'][g] = roster[x]['person']['fullName']
        goalieIDs['pos'][g] = roster[x]['position']['code']
        g = g+1
                  

# // Season Statistics To Date // 
url = 'https://statsapi.web.nhl.com/api/v1/people/'
query = '?hydrate=stats(splits=statsSingleSeason)'


#// Pre allocation of Space for statistics
    
columnNamesG = ['playerID','playerName','evenSaves','evenShots','evenStrengthSavePercentage','games','gamesStarted','goalAgainstAverage',
                           'goalsAgainst','losses','ot','powerPlaySavePercentage','powerPlaySaves','powerPlaySaves','powerPlayShots',
                           'savePercentage','saves','shortHandedSavePercentage','shortHandedSaves','shortHandedShots','shotsAgainst',
                           'shutouts','ties','timeOnIce','timeOnIcePerGame','wins']

columnNamesP = ['playerID','playerName','assists','blocked','evenTimeOnIce','evenTimeOnIcePerGame','faceOffPct','gameWinningGoals','games',
                'goals','hits','overTimeGoals','penaltyMinutes','pim','plusMinus','points','powerPlayGoals','powerPlayPoints','powerPlayTimeOnIce',
                'powerPlayTimeOnIcePerGame','shifts','shortHandedGoals','shortHandedPoints','shortHandedTimeOnIce','shortHandedTimeOnIcePerGame',
                'shotPct','shots','timeOnIce','timeOnIcePerGame']                          

playerStats = pd.DataFrame(np.nan, range(0,numplayers), columns = columnNamesP)
playerStatsG = pd.DataFrame(np.nan, range(0,numplayers), columns = columnNamesG)                          

                           
for x in range (0,numplayers):
   
    playerID = str(int(playerIDs['playerID'][x]))
    url = 'https://statsapi.web.nhl.com/api/v1/people/'
    url = url+playerID+query
    resp = requests.get(url=url)
    playerData = json.loads(resp.text)
    playerStats[columnNamesP[0]][x] = playerIDs['playerID'][x]
    playerStats[columnNamesP[1]][x] = playerIDs['playerName'][x] 
    for i in range (2,len(columnNamesP)):
        playerStats[columnNamesP[i]][x] = (playerData['people'][0]['stats'][0]['splits'][0]['stat'][columnNamesP[i]])

#                           
#for x in range (0,numgoalies):
#   
#    playerID = str(int(goalieIDs['playerID'][x]))
#    url = 'https://statsapi.web.nhl.com/api/v1/people/'
#    url = url+playerID+query
#    resp = requests.get(url=url)
#    playerData = json.loads(resp.text)
#    playerStatsG[columnNamesP[0]][x] = goalieIDs['playerID'][x]
#    playerStatsG[columnNamesP[1]][x] = goalieIDs['playerName'][x] 
#    for i in range (2,len(columnNamesP)):
#        playerStatsG[columnNamesG[i]][x] = (playerData['people'][0]['stats'][0]['splits'][0]['stat'][columnNamesG[i]])
#

## still having problems parsing out goalies data ... WTF is this error
        