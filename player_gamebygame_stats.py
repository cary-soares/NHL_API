# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 19:23:52 2017

@author: Cary
"""
import json
import requests
import pandas as pd
import numpy as np
import datetime

searchTeam = 'OTT'

#// Start by searching for team ID // 

api = 'https://statsapi.web.nhl.com/api/v1/'
apishort = 'https://statsapi.web.nhl.com/'
teams = 'teams'

url = api+teams
resp = requests.get(url=url)
teamData = json.loads(resp.text)
teamData = teamData['teams'][0:]
teamIndex = pd.DataFrame(np.nan, range(0,31), columns=['ID','TeamName'])

for x in range (0,len(teamData)):
    teamIndex['ID'][x] = teamData[x]['franchiseId']
    teamIndex['TeamName'][x] = teamData[x]['abbreviation']


TeamID = np.flatnonzero(teamIndex['TeamName'] == searchTeam)+1
TeamID = str(TeamID[0])

## Search for all game IDs
enddate = str(datetime.datetime.today().strftime('%Y-%m-%d'))
startdate = 'schedule?startDate=2017-10-01&endDate='
team = '&teamId='+TeamID
url = api+startdate+enddate+team

resp = requests.get(url=url)
teamSched = json.loads(resp.text)
numgames = len(teamSched['dates'])

gameIDs = pd.DataFrame(np.nan, range(0,numgames), columns=['gameID','date'])

for x in range(0,numgames):
    gameIDs['gameID'][x] = teamSched['dates'][x]['games'][0]['gamePk']
    gameIDs['date'][x] = teamSched['dates'][x]['date']

#// Search for Team Roster IDs // 
## next step is to grab player IDs from all games

rosterIDs = pd.DataFrame(np.nan, range(0,50), columns=['playerID','playerName','pos'])

for x in range(0,numgames):
    s = api
    ID = str(gameIDs['gameID'][x])
    url = s+'game/'+str(int(gameIDs['gameID'][x]))+'/feed/live'
    resp = requests.get(url=url)
    gameData = json.loads(resp.text)
    
    for i in range(0,23):
        rosterIDs['playerID'][i] = gameData[]
    
  #### this is where IM at
  
    
    

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
                  


url = 'https://statsapi.web.nhl.com/api/v1/people/8475913/stats?stats=gameLog&season=20172018'

resp = requests.get(url=url)
teamData = json.loads(resp.text)

columnNamesP = ['playerID','playerName','gameID','assists','blocked','evenTimeOnIce','evenTimeOnIcePerGame','faceOffPct','gameWinningGoals','games',
                'goals','hits','overTimeGoals','penaltyMinutes','pim','plusMinus','points','powerPlayGoals','powerPlayPoints','powerPlayTimeOnIce',
                'powerPlayTimeOnIcePerGame','shifts','shortHandedGoals','shortHandedPoints','shortHandedTimeOnIce','shortHandedTimeOnIcePerGame',
                'shotPct','shots','timeOnIce','timeOnIcePerGame']                          

playerStats = pd.DataFrame(np.nan, range(0,numplayers), columns = columnNamesP)

