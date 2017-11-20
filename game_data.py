# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:45:05 2017

@author: Cary
"""

import json
import requests
import pandas as pd
import numpy as np

pd.set_option('display.float_format', lambda x: '%.10f' % x)

#// Start by searching for team ID // 
gameIndex = pd.DataFrame(np.nan, range(0,0), columns=['gameID','homeTeam','awayTeam','homeScore','awayScore','OT','shootout','homeShots','awayShots'])

for x in range (1,500):

    url1 = 'http://statsapi.web.nhl.com/api/v1/game/201702'
    url2 = str(x).zfill(4) 
    url3 = '/feed/live'
    url = url1+url2+url3

    resp = requests.get(url=url)
    teamData = json.loads(resp.text)

    gameStats = pd.DataFrame(np.nan, range(0,1), columns=['gameID','homeTeam','awayTeam','homeScore','awayScore','OT','shootout','homeShots','awayShots'])

    gameStats['gameID'][0] = teamData['gamePk']
    gameStats['homeTeam'][0] = teamData['gameData']['teams']['home']['abbreviation']
    gameStats['awayTeam'][0] = teamData['gameData']['teams']['away']['abbreviation']
    gameStats['homeScore'][0] = teamData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
    gameStats['awayScore'][0] = teamData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']
    gameStats['homeShots'][0] = teamData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['shots']
    gameStats['awayShots'][0] = teamData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['shots']
    
    if teamData['liveData']['linescore']['currentPeriod'] == 4:
         gameStats['OT'][0] = 'y'
    else:
        gameStats['OT'][0] = 'n'
        
    if teamData['liveData']['linescore']['currentPeriod'] == 5:
         gameStats['OT'][0] = 'y'
         gameStats['shootout'][0] = 'y'
         if teamData['liveData']['linescore']['shootoutInfo']['away']['scores'] > teamData['liveData']['linescore']['shootoutInfo']['home']['scores']:
             gameStats['awayScore'][0] =  gameStats['awayScore'][0]+1  
         else:
             gameStats['homeScore'][0] =  gameStats['homeScore'][0]+1
                         
    
    gameIndex =  gameIndex.append(gameStats, ignore_index=True)
    print(x)
    
gameIndex.gameID.astype(np.int64)

# example query

massive_wins = gameIndex[(gameIndex['homeScore'] > 2* gameIndex['awayScore']) | (gameIndex['awayScore'] > 2* gameIndex['homeScore'])] 

