# NHL_API

Summary: This library contains python functions to extract data from the NHL's official stats API. In most cases, the functions return data in a pandas Dataframe. 

All functions are stored in the file 'functions.py' (see description below)

Files with names beginning with 'db_' are used to either create or update tables in a MySQL database.   


## functions.py 
- contains several functions that are written to extract player and game statistics data from the NHL's API, which can be found at https://statsapi.web.nhl.com/api/v1/ {followed by a specific GET request} OR http://www.nhl.com/stats/rest/skaters? {followed by a specific GET request}.

__
date_range(start_date, end_date)

Input a start_date and end_date [e.g., date_range('YYYY-MM-DD', 'YYYY-MM-DD')]
Function will return a list in order of all dates between 'start_date' and 'end_date' in YYYY-MM-DD string format.

__
get_adv_stats(start_date, end_date)

Input a start_date and end_date [e.g., date_range('YYYY-MM-DD', 'YYYY-MM-DD')]
Function will return a 94 different advanced stats metrics for each skater (goalies excluded), from each game, within the defined date range. Each game will return a dataframe with each skater as a row and the 94 skater metrics as columns. Data from all games are appended into a single dataframe.   

__
get_games(start_date, end_date)

Input a start_date and end_date [e.g., date_range('YYYY-MM-DD', 'YYYY-MM-DD')]
Function will return all gameIDs (e.g., 2017020001) from the defined date range. 

__
get_games_yest()

Function will return a list of all gameIDs from the day before
This is particularly useful for updating a database with game data on a daily basis.

__
get_game_data(gameID)

Input a gameID (e.g., 2017020001)
Function will return a single dataframe containing all basic stats (goals, assists, PIMs, TOI) for all skaters (home and away).

__
repl_rosterID(df,rosterIDs)

Input a dataframe and the name of a column containing rosterIDs 
Function will return the exact same dataframe with the rosterIDs column converted into player names (firstNameLastName)

__
convert_times(df,col_name)

Input a dataframe and the name of a column (col_name) where time is represented in a MM:SS format
Function will return the exact same dataframe the time column converted to a HH:MM:SS time format. 

__


 





 
