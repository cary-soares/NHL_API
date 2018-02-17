
import json
import requests
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import functools


def date_range(start_date, end_date):

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    r = (end_date+timedelta(days=1)-start_date).days
    dateList = [start_date+timedelta(days=i) for i in range(r)]
    date_strings = [dt.strftime('%Y-%m-%d') for dt in dateList]
    return date_strings


def get_adv_stats(start_date, end_date):
    
    dates = date_range(start_date,end_date)   
    
    colNames1 = ['playerId','gameId','playerName','playerPositionCode','gameDate','teamAbbrev','opponentTeamAbbrev','goals','assists','points','shots','penaltyMinutes','plusMinus',
                 'shootingPctg','gameWinningGoals','otGoals','ppGoals','ppPoints','shGoals','shPoints','shiftsPerGame','timeOnIcePerGame']
    
    colNames2 = ['playerId','assist1st','assist2nd','avgShotLength','penaltiesDrawn']
    
    colNames3 = ['playerId','shotAttempts','shotAttemptsAgainst','shotAttemptsAhead',
                'shotAttemptsBehind','shotAttemptsClose','shotAttemptsFor','shotAttemptsRelPctg','shotAttemptsTied','unblockedShotAttempts',
                'unblockedShotAttemptsAgainst','unblockedShotAttemptsAhead','unblockedShotAttemptsBehind','unblockedShotAttemptsClose','unblockedShotAttemptsFor',
                'unblockedShotAttemptsRelPctg','unblockedShotAttemptsTied']
    
    colNames4 = ['playerId','fiveOnFiveShootingPctg','offensiveZoneFaceoffs','shootingPlusSavePctg','shotAttemptsPctg',
                      'shotAttemptsPctgAhead','shotAttemptsPctgBehind','shotAttemptsPctgClose','shotAttemptsPctgTied','unblockedShotAttemptsPctg','unblockedShotAttemptsPctgAhead',
                      'unblockedShotAttemptsPctgBehind','unblockedShotAttemptsPctgClose','unblockedShotAttemptsPctgTied','zoneStartPctg']  
    
    colNames5 = ['playerId','faceoffLossDefensiveZone','faceoffLossNeutralZone','faceoffLossOffensiveZone','faceoffLossWhenAhead','faceoffLossWhenBehind',
                     'faceoffLossWhenClose','faceoffWinPctg','faceoffWinPctgDefensiveZone','faceoffWinPctgNeutralZone','faceoffWinPctgOffensiveZone','faceoffWins',
                     'faceoffWinsDefensiveZone','faceoffWinsNeutralZone','faceoffWinsOffensiveZone','faceoffWinsWhenAhead','faceoffWinsWhenBehind','faceoffWinsWhenClose','faceoffsTaken']
    
    colNames6 = ['playerId','goalsBackhand','goalsDeflected','goalsSlap','goalsSnap','goalsTipped','goalsWraparound','goalsWrist','missedShots',
                     'missedShotsHitCrossbar','missedShotsHitPost','missedShotsOverNet','missedShotsWideOfNet','shotsBackhand','shotsDeflected','shotsSlap',
                     'shotsSnap','shotsTipped','shotsWraparound','shotsWrist']
    
    
    
    col_list = colNames1 + colNames2[1:] + colNames3[1:] + colNames4[1:] + colNames5[1:] + colNames6[1:] 
    playerStats = pd.DataFrame(np.nan, range(0,0), columns = col_list)
    
    for day in dates:
        start = day
        end = day   
        
        print(day)    
    #Basic
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=true&reportName=skatersummary&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        basicStats = json.loads(resp.text)
        
        num_entries = basicStats['total']-1
        
        playerStats1 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames1)
        
        for i in range(0,num_entries):
            for z in range(0,len(colNames1)):
                 playerStats1[colNames1[z]][i] = basicStats['data'][i][colNames1[z]]
                 
    #SkaterScoring
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=core&isGame=false&reportName=skaterscoring&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        skaterScoring = json.loads(resp.text)
                
        playerStats2 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames2)
        
        for i in range(0,num_entries):
            for z in range(0,len(colNames2)):
                 playerStats2[colNames2[z]][i] = skaterScoring['data'][i][colNames2[z]]
    
    #SkaterShooting
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=shooting&isGame=false&reportName=skatersummaryshooting&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        skaterShooting = json.loads(resp.text)
                
        playerStats3 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames3)
        for i in range(0,num_entries):
            for z in range(0,len(colNames3)):
                playerStats3[colNames3[z]][i] = skaterShooting['data'][i][colNames3[z]]
        
    #SkaterPercentages
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=shooting&isGame=false&reportName=skaterpercentages&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        skaterPercentages = json.loads(resp.text)
                
        playerStats4 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames4)
        for i in range(0,num_entries):
            for z in range(0,len(colNames4)):
                 playerStats4[colNames4[z]][i] = skaterPercentages['data'][i][colNames4[z]]
       
    #Faceoffs
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=core&isGame=false&reportName=faceoffsbyzone&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        faceoffs = json.loads(resp.text)
                
        playerStats5 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames5)
        
        for i in range(0,num_entries):
            for z in range(0,len(colNames5)):
                 playerStats5[colNames5[z]][i] = faceoffs['data'][i][colNames5[z]]
        
    #shotType
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=core&isGame=false&reportName=shottype&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        shottype = json.loads(resp.text)
                
        playerStats6 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames6)
        
        for i in range(0,num_entries):
            for z in range(0,len(colNames6)):
                 playerStats6[colNames6[z]][i] = shottype['data'][i][colNames6[z]]
        
    
      
        ## CONSOLIDATING
        dfs = [playerStats1, playerStats2, playerStats3, playerStats4, playerStats5, playerStats6]
        playerStatsCombine = functools.reduce(lambda left,right: pd.merge(left,right,on='playerId'), dfs)
    
        playerStats = playerStats.append(playerStatsCombine)
    
    ## NEED TO Rearrage column names and also go through it to filter what is actually needed
    playerStats = playerStats[col_list]
    return(playerStats)
    
    
def get_games(start_date,end_date):
    
    """returns gameIDs from the defined date range as a list"""
    
    url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}'.format(start_date,end_date)
    resp = requests.get(url=url)
    gameSched = json.loads(resp.text)
    gameIDs = []
    
    for day in range(0,len(gameSched['dates'])):
        
        games = gameSched['dates'][day]['games']
    
        for x in range(0,len(games)):
            gameID = games[x]['gamePk']
            gameIDs.append(gameID)
        
    return(gameIDs)


def get_games_yest():
    
    """returns gameIDs only for the previous day"""
    
    yesterday = str(date.today() - timedelta(1))
    url = 'https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}'.format(yesterday,yesterday)
    resp = requests.get(url=url)
    gameSched = json.loads(resp.text)
    games = gameSched['dates'][0]['games']
    gameIDs = []
    
    for x in range(0,len(games)):
        gameID = games[x]['gamePk']
        gameIDs.append(gameID)
        
    return(gameIDs)


def get_game_data(gameID):
    
    """returns home and away player statistics in a single dataframe"""
    # gets game data from API
    url = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(gameID)
    resp = requests.get(url=url)
    gameData = json.loads(resp.text)
    
    #Build an Empty Data Frame to hold the player statistics data
    columnNamesP = ['gameID','rosterID','home','away','assists','blocked','evenTimeOnIce','faceOffWins','faceoffTaken', 'giveaways','goals',             
                    'hits','penaltyMinutes','plusMinus','powerPlayAssists', 'powerPlayGoals','powerPlayTimeOnIce','shortHandedAssists','shortHandedGoals','shortHandedTimeOnIce',
                    'shots','takeaways','timeOnIce','points'] 
    
    playerStatsFULL = pd.DataFrame(np.nan, range(0,0), columns = columnNamesP)
    
   ## Start with home team 
    rosterIDs = gameData['liveData']['boxscore']['teams']['home']['skaters']
    scratches = gameData['liveData']['boxscore']['teams']['home']['scratches']
    for scratch in scratches:
        rosterIDs.remove(scratch)
        
    homeStats = pd.DataFrame(np.nan, range(0,len(rosterIDs)), columns = columnNamesP)
    
    # populate homeStats with home player game stats
    for i in range(0,len(rosterIDs)):
               homeStats[columnNamesP[0]][i] = gameID
               homeStats[columnNamesP[1]][i] = int(rosterIDs[i])  
               homeStats[columnNamesP[2]][i] = gameData['gameData']['teams']['home']['abbreviation']
               homeStats[columnNamesP[3]][i] = gameData['gameData']['teams']['away']['abbreviation']
               for z in range(4,len(columnNamesP)-1):
                   if gameData['liveData']['boxscore']['teams']['home']['players']['ID'+str(rosterIDs[i])]['position']['code'] == 'N/A':
                       continue 
                   else:
                       homeStats[columnNamesP[z]][i] = gameData['liveData']['boxscore']['teams']['home']['players']['ID'+str(rosterIDs[i])]['stats']['skaterStats'][columnNamesP[z]]
               homeStats[columnNamesP[z+1]][i] =  homeStats['goals'][i]+homeStats['assists'][i]
    
    ## away team 
    rosterIDs = gameData['liveData']['boxscore']['teams']['away']['skaters']
    scratches = gameData['liveData']['boxscore']['teams']['away']['scratches']
    for scratch in scratches:
        rosterIDs.remove(scratch)
        
    awayStats = pd.DataFrame(np.nan, range(0,len(rosterIDs)), columns = columnNamesP)
    
    # populate awayStats with away player game stats
    for i in range(0,len(rosterIDs)):
               awayStats[columnNamesP[0]][i] = gameID
               awayStats[columnNamesP[1]][i] = int(rosterIDs[i])
               awayStats[columnNamesP[2]][i] = gameData['gameData']['teams']['home']['abbreviation']
               awayStats[columnNamesP[3]][i] = gameData['gameData']['teams']['away']['abbreviation']
               for z in range(4,len(columnNamesP)-1):
                   if gameData['liveData']['boxscore']['teams']['away']['players']['ID'+str(rosterIDs[i])]['position']['code'] == 'N/A':
                       continue 
                   else:
                       awayStats[columnNamesP[z]][i] = gameData['liveData']['boxscore']['teams']['away']['players']['ID'+str(rosterIDs[i])]['stats']['skaterStats'][columnNamesP[z]]
               awayStats[columnNamesP[z+1]][i] =  awayStats['goals'][i]+homeStats['assists'][i]
  
    
    playerStatsFULL = playerStatsFULL.append(homeStats, ignore_index = True)
    playerStatsFULL = playerStatsFULL.append(awayStats, ignore_index = True)
    
    return(playerStatsFULL)


def repl_rosterID(df,rosterIDs):
    
    """takes a column of rosterIDs and replaces with the player Name"""
    
    for i in range(0,len(df[rosterIDs])):
        api = 'https://statsapi.web.nhl.com/api/v1/people/'
        url = api+str(int(df[rosterIDs][i]))
        resp = requests.get(url=url)
        playerData = json.loads(resp.text)
        playerName = playerData['people'][0]['firstName']+playerData['people'][0]['lastName'] 
        df[rosterIDs][i] = playerName
    
def convert_times(df,col_name):
    
    """converts a time column from a dataframe to format HH:MM:SS"""
    
    for i in range(0,len(df)):
        if len(df[col_name][i]) == 4:
            df[col_name][i] = '00:0' + df[col_name][i]
        else:
            df[col_name][i] = '00:' + df[col_name][i]
            
            
def convert_IDs(df,col_name):
   
     """converts a column of IDs from numeric to string"""
     df[col_name] = df[col_name].astype(int)
     df[col_name] = df[col_name].astype(str)
           

def get_player_GBG_data(start_date,end_date):
    
    gamesIDs = get_games(start_date,end_date)
    columnNamesP = ['gameID','rosterID','assists','blocked','evenTimeOnIce','faceOffWins','faceoffTaken', 'giveaways','goals',             
                    'hits','penaltyMinutes','plusMinus','powerPlayAssists', 'powerPlayGoals','powerPlayTimeOnIce','shortHandedAssists','shortHandedGoals','shortHandedTimeOnIce',
                    'shots','takeaways','timeOnIce','points']
    playerStats = pd.DataFrame(np.nan, range(0,0), columns = columnNamesP) 
    
    counter = 1
    
    for game in gamesIDs:
        print(counter)
        player_data = get_game_data(game)
        playerStats = playerStats.append(player_data, ignore_index = True)
        counter += 1   
        
    ##reorder columns for mySQL export
    playerStats = playerStats[['gameID','home','away','rosterID','goals','assists','points','shots','penaltyMinutes','plusMinus','blocked','hits','giveaways','takeaways','faceOffWins','faceoffTaken',
                 'timeOnIce','evenTimeOnIce','powerPlayTimeOnIce','shortHandedTimeOnIce','powerPlayGoals','powerPlayAssists','shortHandedGoals','shortHandedAssists',]]   
    
    ##alter column format for mySQL export
    
    convert_times(playerStats,'evenTimeOnIce')
    convert_times(playerStats,'powerPlayTimeOnIce')
    convert_times(playerStats,'shortHandedTimeOnIce')
    convert_times(playerStats, 'timeOnIce')
    convert_IDs(playerStats,'gameID')
    convert_IDs(playerStats,'rosterID')
    
    playerList = list(set(playerStats.rosterID))
    
    return(playerStats)
    
    
def get_player_GBG_data_yest():
    
    gamesIDs = get_games_yest()
    columnNamesP = ['gameID','rosterID','assists','blocked','evenTimeOnIce','faceOffWins','faceoffTaken', 'giveaways','goals',             
                    'hits','penaltyMinutes','plusMinus','powerPlayAssists', 'powerPlayGoals','powerPlayTimeOnIce','shortHandedAssists','shortHandedGoals','shortHandedTimeOnIce',
                    'shots','takeaways','timeOnIce','points']
    playerStats = pd.DataFrame(np.nan, range(0,0), columns = columnNamesP) 
    
    for game in gamesIDs:
        player_data = get_game_data(game)
        playerStats = playerStats.append(player_data, ignore_index = True)
    
    ##reorder columns for mySQL export
    playerStats = playerStats[['gameID','home','away','rosterID','goals','assists','points','shots','penaltyMinutes','plusMinus','blocked','hits','giveaways','takeaways','faceOffWins','faceoffTaken',
                 'timeOnIce','evenTimeOnIce','powerPlayTimeOnIce','shortHandedTimeOnIce','powerPlayGoals','powerPlayAssists','shortHandedGoals','shortHandedAssists',]] 
    
    ##alter column format for mySQL export
    convert_times(playerStats,'evenTimeOnIce')
    convert_times(playerStats,'powerPlayTimeOnIce')
    convert_times(playerStats,'shortHandedTimeOnIce')
    convert_times(playerStats, 'timeOnIce')
    convert_IDs(playerStats,'gameID')
    convert_IDs(playerStats,'rosterID')
    
    return(playerStats)

#### Next on the list


def get_event_data(gameID):
    
    url = 'https://statsapi.web.nhl.com/api/v1/game/{}/feed/live'.format(gameID)
    columns = ['gameID','teamID','period','time','event_type','penalty_type','coor_x','coor_y','player','opponent']
    event_data = pd.DataFrame(np.nan, range(0,0), columns)
    missing_data = pd.DataFrame(np.nan, range(0,0), columns=['gameID'])
    missing_games = 0
    
    resp = requests.get(url=url)
    gameData = json.loads(resp.text)   
    
    event_total = len(gameData['liveData']['plays']['allPlays'])
       
    if event_total < 1:
        missing_data['gameID'][missing_games] = int(gameData['gameData']['game']['pk'])
        missing_games = missing_games+1
    else:
        per_1_plays = list(gameData['liveData']['plays']['playsByPeriod'][0]['plays'])
        per_2_plays = list(gameData['liveData']['plays']['playsByPeriod'][1]['plays'])
        per_3_plays = list(gameData['liveData']['plays']['playsByPeriod'][2]['plays'])
       
    
    if len(gameData['liveData']['plays']['playsByPeriod']) > 3:
           per_4_plays = list(gameData['liveData']['plays']['playsByPeriod'][3]['plays'])
        
    for i in range(0,event_total):
        if len(gameData['liveData']['plays']['allPlays'][i]) == 5: 
            event = pd.DataFrame(np.nan, range(0,1), columns=['gameID','teamID','period','time','event_type','penalty_type','coor_x','coor_y','player', 'opponent'])
            event['gameID'] = int(gameData['gameData']['game']['pk'])
            event['teamID'] = int(gameData['liveData']['plays']['allPlays'][i]['team']['id'])
            if i in per_1_plays:
                event['period'] = 1
            elif i in per_2_plays:
                event['period'] = 2
            elif i in per_3_plays:
                event['period'] = 3
            elif i in per_4_plays:
                event['period'] = 4
            else:
                event['period'] = 5
        
            event['time'] = gameData['liveData']['plays']['allPlays'][i]['about']['periodTime']
            event['event_type'] = gameData['liveData']['plays']['allPlays'][i]['result']['eventTypeId']
            if event['event_type'][0] == 'PENALTY':
                event['penalty_type'] = gameData['liveData']['plays']['allPlays'][i]['result']['penaltySeverity']
            else:
                event['penalty_type'] = np.nan
            
            if len(gameData['liveData']['plays']['allPlays'][i]['coordinates']) == 0:
                 event['coor_x'] = np.nan
                 event['coor_y'] = np.nan
            else: 
                event['coor_x'] = gameData['liveData']['plays']['allPlays'][i]['coordinates']['x']
                event['coor_y'] = gameData['liveData']['plays']['allPlays'][i]['coordinates']['y']
            
            event['player'] = gameData['liveData']['plays']['allPlays'][i]['players'][0]['player']['id']
            if len(gameData['liveData']['plays']['allPlays'][i]['players']) > 1:
                event['opponent'] = gameData['liveData']['plays']['allPlays'][i]['players'][1]['player']['id']
            
            event_data = event_data.append(event)
            
    event_data = event_data[['gameID','teamID','period','time','event_type','penalty_type','coor_x','coor_y','player', 'opponent']]
    event_data = event_data.reset_index(drop=True)
         
    return(event_data,missing_data)


def get_event_data_yest():
    gameIDs = get_games_yest()
    columns = ['gameID','teamID','period','time','event_type','penalty_type','coor_x','coor_y','player','opponent']
    event_data = pd.DataFrame(np.nan, range(0,0), columns)
    missing_data = pd.DataFrame(np.nan, range(0,0), columns=['gameID'])
        
    for game in gameIDs:
        print(game)
        gettuple = get_event_data(game)
        eventdata = pd.DataFrame(gettuple[0])
        missingdata = pd.DataFrame(gettuple[1])
        if len(missingdata) > 0:
            missing_data = missing_data.append(missingdata, ignore_index = True)
        
        event_data = event_data.append(eventdata, ignore_index = True)
        
    
    return(event_data,missing_data)


def get_event_data_daterange(start_date,end_date):
    
    """ collects event data (shots, missed shots, blocks, hits, penalties) from all games in the date range and returns
    it in a single dataframe"""
    
    gameIDs = get_games(start_date,end_date)
    columns = ['gameID','teamID','period','time','event_type','penalty_type','coor_x','coor_y','player','opponent']
    event_data = pd.DataFrame(np.nan, range(0,0), columns)
    missing_data = pd.DataFrame(np.nan, range(0,0), columns=['gameID'])
        
    for game in gameIDs:
        print(game)
        gettuple = get_event_data(game)
        eventdata = pd.DataFrame(gettuple[0])
        missingdata = pd.DataFrame(gettuple[1])
        if len(missingdata) > 0:
            missing_data = missing_data.append(missingdata, ignore_index = True)
        
        event_data = event_data.append(eventdata, ignore_index = True)
        
    
    return(event_data,missing_data)

            
        

### disables a copy warning from appearing in the console
pd.options.mode.chained_assignment = None  # default='warn'