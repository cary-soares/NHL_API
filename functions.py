
import json
import requests
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
import functools
import math


def date_range(start_date, end_date):
    
    """ Returs a list of all dates between Start and End in YYYY-MM-DD string format"""

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    r = (end_date+timedelta(days=1)-start_date).days
    dateList = [start_date+timedelta(days=i) for i in range(r)]
    date_strings = [dt.strftime('%Y-%m-%d') for dt in dateList]
    return date_strings


def get_adv_stats(start_date, end_date):
    
    """ This function will pull 94 different player metrics for each player and from each game within the date range"""
    """Since the official stats API ('statsapi.web.nhl.com/api/v1/') does not contain advanced player stats, a different url is used"""
      
  #establishing the column names for the DataFrames that will eventually consolidate to a single 'playerStats' dataframe
  
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
    
    
## loop to gather player metrics from each day and consolidate into a single dataframe

    dates = date_range(start_date,end_date) 
    
    for day in dates:
        start = day
        end = day   
        
        print(day)    
        
    #Basic Stats
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=basic&isGame=true&reportName=skatersummary&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        basicStats = json.loads(resp.text)
        
        num_entries = basicStats['total']-1
        
        playerStats1 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames1)
        
        for i in range(0,num_entries):
            for z in range(0,len(colNames1)):
                 playerStats1[colNames1[z]][i] = basicStats['data'][i][colNames1[z]]
                 
    #SkaterScoring Stats
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=core&isGame=false&reportName=skaterscoring&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        skaterScoring = json.loads(resp.text)
                
        playerStats2 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames2)
        
        for i in range(0,num_entries):
            for z in range(0,len(colNames2)):
                 playerStats2[colNames2[z]][i] = skaterScoring['data'][i][colNames2[z]]
    
    #SkaterShooting Stats
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=shooting&isGame=false&reportName=skatersummaryshooting&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        skaterShooting = json.loads(resp.text)
                
        playerStats3 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames3)
        for i in range(0,num_entries):
            for z in range(0,len(colNames3)):
                playerStats3[colNames3[z]][i] = skaterShooting['data'][i][colNames3[z]]
        
    #SkaterPercentage Stats
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=shooting&isGame=false&reportName=skaterpercentages&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        skaterPercentages = json.loads(resp.text)
                
        playerStats4 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames4)
        for i in range(0,num_entries):
            for z in range(0,len(colNames4)):
                 playerStats4[colNames4[z]][i] = skaterPercentages['data'][i][colNames4[z]]
       
    #Faceoff Stats
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=core&isGame=false&reportName=faceoffsbyzone&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        faceoffs = json.loads(resp.text)
                
        playerStats5 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames5)
        
        for i in range(0,num_entries):
            for z in range(0,len(colNames5)):
                 playerStats5[colNames5[z]][i] = faceoffs['data'][i][colNames5[z]]
        
    #shotType Stats
        url = 'http://www.nhl.com/stats/rest/skaters?isAggregate=false&reportType=core&isGame=false&reportName=shottype&cayenneExp=gameDate%3E=%22{}%22%20and%20gameDate%3C=%22{}%2023:59:59%22%20and%20gameTypeId=2'.format(start,end)
        resp = requests.get(url=url)
        shottype = json.loads(resp.text)
                
        playerStats6 = pd.DataFrame(np.nan, range(0,num_entries), columns = colNames6)
        
        for i in range(0,num_entries):
            for z in range(0,len(colNames6)):
                 playerStats6[colNames6[z]][i] = shottype['data'][i][colNames6[z]]
        
    
      
    ## CONSOLIDATING dfs 
        dfs = [playerStats1, playerStats2, playerStats3, playerStats4, playerStats5, playerStats6]
        playerStatsCombine = functools.reduce(lambda left,right: pd.merge(left,right,on='playerId'), dfs)
    
        playerStats = playerStats.append(playerStatsCombine)
    
    ## Rearrage columns for a more simple navigation
    playerStats = playerStats[col_list].reset_index(drop=True)
    
    #convert column types for export to mySQL
    convert_times_drop(playerStats,'gameDate')
    convert_times_S_DT(playerStats, 'timeOnIcePerGame')
    playerStats['playerId'] = playerStats['playerId'].astype(int).astype(str)
    playerStats['gameId'] = playerStats['gameId'].astype(int).astype(str)
    
    
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
        if (df[col_name][i] == 4):
            df[col_name][i] = '00:0' + df[col_name][i]
        else:
            df[col_name][i] = '00:' + df[col_name][i]
            

def convert_times_S_DT(df,col_name):                
    """converts a time column from a dataframe to format HH:MM:SS"""
    
    for i in range(0,len(df)):
        time_format = 'HH:MM:SS'
        time = df[col_name][i]
        
        if time > 3600: 
            hours = str(math.floor(time/3600))
            minutes = str(round((time%3600)/60))
            seconds = str(round((time%3600)%60))
        else:
            hours = '00'
            minutes = str(math.floor(time/60))
            seconds = str(round(int(time%60)))  
        
        if hours == '00':
            time_format = time_format.replace('HH', hours)
        else:
            time_format = time_format.replace('HH', '0'+str(hours))
        
        if len(minutes) == 2:
            time_format = time_format.replace('MM', str(minutes))
        else:
            time_format = time_format.replace('MM', '0'+str(minutes))
        
        if len(seconds) == 2:
            time_format = time_format.replace('SS', str(seconds))
        else:
            time_format = time_format.replace('SS', '0'+str(seconds))
        
        df[col_name][i]  = time_format 
            
def convert_times_drop(df,col_name):                
    """converts a time column from a dataframe to format HH:MM:SS"""
    
    for i in range(0,len(df)):
        time = df[col_name][i]
        time = time[0:10]
        df[col_name][i]  = time

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
    columns = ['gameID','teamID','period','time','eventType','secondaryType','coor_x','coor_y','player','opponent']
    event_data = pd.DataFrame(np.nan, range(0,0), columns)
    missing_data = pd.DataFrame(np.nan, range(0,1), columns=['gameID'])
    missing_games = 0
    
    resp = requests.get(url=url)
    gameData = json.loads(resp.text)   
    
    try:
        event_total = len(gameData['liveData']['plays']['allPlays'])
        
        if event_total < 1:
            missing_data['gameID'][missing_games] = int(gameID)
            missing_games = missing_games+1
        else:
            per_1_plays = list(gameData['liveData']['plays']['playsByPeriod'][0]['plays'])
            per_2_plays = list(gameData['liveData']['plays']['playsByPeriod'][1]['plays'])
            per_3_plays = list(gameData['liveData']['plays']['playsByPeriod'][2]['plays'])
           
            home_team = gameData['liveData']['boxscore']['teams']['home']['team']['abbreviation']
            away_team = gameData['liveData']['boxscore']['teams']['away']['team']['abbreviation']
            home_list = gameData['liveData']['boxscore']['teams']['home']['skaters']
        
            if len(gameData['liveData']['plays']['playsByPeriod']) > 3:
                   per_4_plays = list(gameData['liveData']['plays']['playsByPeriod'][3]['plays'])
                
            for i in range(0,event_total):
                if len(gameData['liveData']['plays']['allPlays'][i]) == 5: 
                    event = pd.DataFrame(np.nan, range(0,1), columns=['gameID','teamID','period','time','eventType','secondaryType','coor_x','coor_y','player', 'opponent'])
                    event['gameID'] = str(int(gameData['gameData']['game']['pk']))
                    event['teamID'] = str(int(gameData['liveData']['plays']['allPlays'][i]['team']['id']))
                    if i in per_1_plays:
                        event['period'] = str(1)
                    elif i in per_2_plays:
                        event['period'] = str(2)
                    elif i in per_3_plays:
                        event['period'] = str(3)
                    elif i in per_4_plays:
                        event['period'] = str(4)
                    else:
                        event['period'] = str(5)
                
                    event['time'] = '00:'+ gameData['liveData']['plays']['allPlays'][i]['about']['periodTime']
                    event['eventType'] = gameData['liveData']['plays']['allPlays'][i]['result']['eventTypeId']
                    
                    if (len(gameData['liveData']['plays']['allPlays'][i]['result']) == 5) | (event['eventType'][0] == 'GOAL'):
                        event['secondaryType'] = gameData['liveData']['plays']['allPlays'][i]['result']['secondaryType']
                    else:
                        event['secondaryType'] = np.nan
                             
                    if event['eventType'][0] == 'PENALTY':
                        event['secondaryType'] = gameData['liveData']['plays']['allPlays'][i]['result']['penaltySeverity']
                    
                    if len(gameData['liveData']['plays']['allPlays'][i]['coordinates']) < 2:
                         event['coor_x'] = np.nan
                         event['coor_y'] = np.nan
                    else: 
                        event['coor_x'] = gameData['liveData']['plays']['allPlays'][i]['coordinates']['x']
                        event['coor_y'] = gameData['liveData']['plays']['allPlays'][i]['coordinates']['y']
                    
                    event['player'] = int(gameData['liveData']['plays']['allPlays'][i]['players'][0]['player']['id'])
                   
                    if len(gameData['liveData']['plays']['allPlays'][i]['players']) > 1:
                        event['opponent'] = int(gameData['liveData']['plays']['allPlays'][i]['players'][1]['player']['id'])
                    
                    event_data = event_data.append(event)
            
            event_data['playerTeam'] = event_data['player'].isin(home_list)
            team = {True:home_team, False:away_team}
            event_data['playerTeam'] = event_data['playerTeam'].map(team) 
            
            event_data['opponentTeam'] = event_data['opponent'].isin(home_list)
            event_data['opponentTeam'] = event_data['opponentTeam'].map(team) 
            event_data.ix[event_data['opponent'].isnull(), 'opponentTeam'] = np.nan
            
            event_data['player'].astype(str)
            event_data['opponent'].astype(str)              
            
            event_data = event_data[['gameID','teamID','period','time','eventType','secondaryType','coor_x','coor_y','player','opponent','playerTeam','opponentTeam']]
            event_data = event_data.reset_index(drop=True)
    
    except:
        missing_data['gameID'][missing_games] = int(gameID)
        missing_games = missing_games+1
            
    return(event_data,list(missing_data['gameID']))

## need to refine yest 
def get_event_data_yest():
    gameIDs = get_games_yest()
    columns = ['gameID','teamID','period','time','eventType','secondaryType','coor_x','coor_y','player','opponent','playerTeam','opponentTeam']
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
    columns = ['gameID','teamID','period','time','eventType','secondaryType','coor_x','coor_y','player','opponent','playerTeam','opponentTeam']
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

def get_player_info(playerId):

    cols = ['id','fullName','birthDate','birthCity','birthCountry','shootsCatches','position','teamId','team','birthStateProvince']
    
    url = 'https://statsapi.web.nhl.com/api/v1/people/{}'.format(str(playerId))
    resp = requests.get(url=url)
    playerInfoJSON = json.loads(resp.text)
    
    playerInfo = pd.DataFrame(np.nan, range(0,1), columns = cols)
    playerInfo['id'] = playerId
    
    for i in range(1,len(cols)-4):
        playerInfo[cols[i]] = playerInfoJSON['people'][0][cols[i]]
    
    playerInfo['position'] = playerInfoJSON['people'][0]['primaryPosition']['code']
    if playerInfoJSON['people'][0]['active'] is False:
        playerInfo['teamId'] = np.nan   
        playerInfo['team'] = np.nan
    else:
        playerInfo['teamId'] = playerInfoJSON['people'][0]['currentTeam']['id']   
        playerInfo['team'] = playerInfoJSON['people'][0]['currentTeam']['name']
    
    NA = ['USA','CAN']
    
    if playerInfo.birthCountry[0] in NA:
        playerInfo['birthStateProvince'] = playerInfoJSON['people'][0]['birthStateProvince']
        
    return(playerInfo)

#Creat player df for Database

colMaster = ['id','fullName','birthDate','birthCity','birthStateProvince','birthCountry','shootsCatches','position','teamId','team']
playerInfoFULL = pd.DataFrame(np.nan, range(0,0), columns = colMaster)

for player in players:
    print(player)
    data = get_player_info(player)
    playerInfoFULL = playerInfoFULL.append(data)
    
playerInfoFULL = playerInfoFULL[colMaster]
playerInfoFULL['teamId'] = playerInfoFULL['teamId'].fillna(0).astype(str) 
    
    
    
    
### disables a copy warning from appearing in the console
pd.options.mode.chained_assignment = None  # default='warn'


