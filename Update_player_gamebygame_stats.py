# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 21:17:34 2017

@author: Cary
"""

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


# path for file export
path = 'C:\\Users\\Cary\\Desktop\\NHL_API\\Data_test\\'

#load team_list
team_list = pd.read_csv('teams.csv', header=None)

#loop through teams
for t in range(0,len(team_list)):
#for t in range(0,1):    
    searchTeam = team_list[0][t]
    TeamID = str(team_list[1][t])
    
    # Reloading files from csv
    locate = 'C:\\Users\\Cary\\Desktop\\NHL_API\\data_test\\'+searchTeam+'_stats.csv'
    playerStatsFULL = pd.read_csv(locate,sep='\t')
    playerStatsFULL = playerStatsFULL.drop(playerStatsFULL.columns[0], axis=1)
    
    api = 'https://statsapi.web.nhl.com/api/v1/'
    apishort = 'https://statsapi.web.nhl.com/'
    
    ## Search for all game IDs
    enddate = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    startdate = 'schedule?startDate=2017-10-01&endDate='
    team = '&teamId='+TeamID
    url = api+startdate+enddate+team
    
    resp = requests.get(url=url)
    teamSched = json.loads(resp.text)
    numgames = len(teamSched['dates'])
    
    gameIDs = pd.DataFrame(np.nan, range(0,numgames), columns=['gameID','date','oppTeamID','home'])
    
    for x in range(0,numgames):
        gameIDs['gameID'][x] = teamSched['dates'][x]['games'][0]['gamePk']
        gameIDs['date'][x] = teamSched['dates'][x]['date']
        if teamSched['dates'][x]['games'][0]['teams']['away']['team']['id'] == int(TeamID):
            gameIDs['oppTeamID'][x] = teamSched['dates'][x]['games'][0]['teams']['home']['team']['id']
            gameIDs['home'][x] = 0
        else:
            gameIDs['oppTeamID'][x] = teamSched['dates'][x]['games'][0]['teams']['away']['team']['id'] 
            gameIDs['home'][x] = 1
                
    
    #// Search for Team Roster IDs // 
    ## next step is to grab player IDs from all games
    
    columnNamesP = ['gameID','gameNumb','rosterID','assists','blocked','evenTimeOnIce','faceOffWins','faceoffTaken', 'giveaways','goals',             
                    'hits','penaltyMinutes','plusMinus','powerPlayAssists', 'powerPlayGoals','powerPlayTimeOnIce','shortHandedAssists','shortHandedGoals','shortHandedTimeOnIce',
                    'shots','takeaways','timeOnIce','points'] 
      
    ## find unique gameID and start from there
    oldGameIDs = list(set(playerStatsFULL.gameID))
    
    for x in range(len(oldGameIDs),len(gameIDs)):
        print(x)
        s = api
        ID = str(gameIDs['gameID'][x])
        url = s+'game/'+str(int(gameIDs['gameID'][x]))+'/feed/live'
        resp = requests.get(url=url)
        gameData = json.loads(resp.text)
                
        if gameData['liveData']['boxscore']['teams']['away']['team']['abbreviation'] == searchTeam:
            skaters = len(gameData['liveData']['boxscore']['teams']['away']['skaters'])-1
            rosterIDs = gameData['liveData']['boxscore']['teams']['away']['skaters']
            playerStats = pd.DataFrame(np.nan, range(0,len(rosterIDs)), columns = columnNamesP)
            for i in range(0,len(rosterIDs)):
                playerStats[columnNamesP[0]][i] = ID 
                playerStats[columnNamesP[1]][i] = x 
                playerStats[columnNamesP[2]][i] = int(rosterIDs[i])       
                for z in range(3,len(columnNamesP)-1):
                    if gameData['liveData']['boxscore']['teams']['away']['players']['ID'+str(rosterIDs[i])]['position']['code'] == 'N/A':
                        continue 
                    else:
                        playerStats[columnNamesP[z]][i] = gameData['liveData']['boxscore']['teams']['away']['players']['ID'+str(rosterIDs[i])]['stats']['skaterStats'][columnNamesP[z]]
                    playerStats[columnNamesP[z+1]][i] =  playerStats['goals'][i]+playerStats['assists'][i]
        
        else:    
            skaters = len(gameData['liveData']['boxscore']['teams']['home']['skaters'])-1
            rosterIDs = gameData['liveData']['boxscore']['teams']['home']['skaters']
            playerStats = pd.DataFrame(np.nan, range(0,len(rosterIDs)), columns = columnNamesP)
            for i in range(0,len(rosterIDs)):
                playerStats[columnNamesP[0]][i] = ID
                playerStats[columnNamesP[1]][i] = x            
                playerStats[columnNamesP[2]][i] = int(rosterIDs[i])           
                for z in range(3,len(columnNamesP)-1):
                    if gameData['liveData']['boxscore']['teams']['home']['players']['ID'+str(rosterIDs[i])]['position']['code'] == 'N/A':
                        continue 
                    else:
                        playerStats[columnNamesP[z]][i] = gameData['liveData']['boxscore']['teams']['home']['players']['ID'+str(rosterIDs[i])]['stats']['skaterStats'][columnNamesP[z]]
                    playerStats[columnNamesP[z+1]][i] =  playerStats['goals'][i]+playerStats['assists'][i]       
            
        playerStatsFULL = playerStatsFULL.append(playerStats)
        del rosterIDs
        del playerStats
    
    # to remove instances where player was a healthy scratch, i dropped all rows that contain empty values (nan)     
    playerStatsFULL = playerStatsFULL.dropna()
    
    # update the rosterIDs with player names
    allPlayerIDs = list(set(playerStatsFULL.rosterID))
    roster = pd.DataFrame(np.nan, range(0,len(allPlayerIDs)), columns = ['playerID','playerName'])
    
    for i in range(0,len(allPlayerIDs)):
        url = api+'/people/'+str(int(allPlayerIDs[i]))
        resp = requests.get(url=url)
        playerData = json.loads(resp.text)
        playerName = playerData['people'][0]['firstName']+playerData['people'][0]['lastName'] 
        roster['playerID'][i] = int(allPlayerIDs[i])
        roster['playerName'][i] = playerName
    
    filename = searchTeam+'_roster.csv'        
    roster.to_csv(path+filename, sep='\t',encoding='utf-8')
    
    filename = searchTeam+'_stats.csv' 
    playerStatsFULL.to_csv(path+filename, sep='\t', encoding='utf-8')
    
    filename = searchTeam+'_gamelist.csv'
    gameIDs.to_csv(path+filename,sep='\t', encoding='utf-8')
    
#    for i in range(0,len(allPlayerIDs)):
#        playerStatsFULL = playerStatsFULL.replace(int(roster['playerID'][i]),roster['playerName'][i])
        

    
    
