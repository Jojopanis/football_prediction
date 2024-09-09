import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from functools import reduce
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score



def load_df():
    df = pd.read_csv('db/dataset.csv')
    matches = df[['Date','HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']]
    matches = matches.dropna()
    matches = pd.get_dummies(matches, columns=['FTR'])
    print(matches.head())
    return matches

def get_20_10_5_home_last_matches(matches):
# Getting the 20 lasts games played at home for each team
    last_home_20 = matches.groupby('HomeTeam').head(20)
    last_home_20.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_home_20 = last_home_20.drop(columns=['Date','AwayTeam'])
    last_home_20[['Loose', 'Draw', 'Win']] = last_home_20[['Loose', 'Draw', 'Win']].astype(int)
    last_home_20 = last_home_20.groupby('HomeTeam').mean()
    last_home_20 = last_home_20.add_suffix('_last_home_20')
# Getting the 10 lasts games played at home for each team
    last_home_10 = matches.groupby('HomeTeam').head(10)
    last_home_10.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_home_10 = last_home_10.drop(columns=['Date','AwayTeam'])
    last_home_10[['Loose', 'Draw', 'Win']] = last_home_10[['Loose', 'Draw', 'Win']].astype(int)
    last_home_10 = last_home_10.groupby('HomeTeam').mean()
    last_home_10 = last_home_10.add_suffix('_last_home_10')
# Getting the 20 lasts games played at home for each team
    last_home_5 = matches.groupby('HomeTeam').head()
    last_home_5.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_home_5 = last_home_5.drop(columns=['Date','AwayTeam'])
    last_home_5[['Loose', 'Draw', 'Win']] = last_home_5[['Loose', 'Draw', 'Win']].astype(int)
    last_home_5 = last_home_5.groupby('HomeTeam').mean()
    last_home_5 = last_home_5.add_suffix('_last_home_5')
# Merging all the df into a single one   
    dfs = [last_home_20,last_home_10,last_home_5]
    team_home_stats = reduce(lambda left, right : pd.merge(left,right, on=['HomeTeam'],how='outer'), dfs)
    return team_home_stats


def get_20_10_5_away_last_matches(matches):
# Getting the 20 lasts games played away for each team
    last_away_20 = matches.groupby('AwayTeam').head(20)
    last_away_20.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_away_20 = last_away_20.drop(columns=['Date','HomeTeam'])
    last_away_20[['Loose', 'Draw', 'Win']] = last_away_20[['Loose', 'Draw', 'Win']].astype(int)
    last_away_20 = last_away_20.groupby('AwayTeam').mean()
    last_away_20 = last_away_20.add_suffix('_last_away_20')
# Getting the 10 lasts games played away for each team
    last_away_10 = matches.groupby('AwayTeam').head(10)
    last_away_10.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_away_10 = last_away_10.drop(columns=['Date','HomeTeam'])
    last_away_10[['Loose', 'Draw', 'Win']] = last_away_10[['Loose', 'Draw', 'Win']].astype(int)
    last_away_10 = last_away_10.groupby('AwayTeam').mean()
    last_away_10 = last_away_10.add_suffix('_last_away_10')
# Getting the 5 lasts games played away for each team
    last_away_5 = matches.groupby('AwayTeam').head()
    last_away_5.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_away_5 = last_away_5.drop(columns=['Date','HomeTeam'])
    last_away_5[['Loose', 'Draw', 'Win']] = last_away_5[['Loose', 'Draw', 'Win']].astype(int)
    last_away_5 = last_away_5.groupby('AwayTeam').mean()
    last_away_5 = last_away_5.add_suffix('_last_away_5')
# Merging all the df into a single one   
    dfs = [last_away_20,last_away_10,last_away_5]
    team_away_stats = reduce(lambda left, right : pd.merge(left,right, on=['AwayTeam'],how='outer'), dfs)
    return team_away_stats

def getting_matches_data():
    match_data = pd.read_csv('db/dataset.csv')
    match_data = match_data[['Date','HomeTeam','AwayTeam','FTR']]
    return match_data

def merging_stats_to_match(team_home_stats, team_away_stats, match_data):
    final_data = pd.merge(match_data, team_home_stats, on=['HomeTeam'], how='outer')
    print(final_data)
    final_data = pd.merge(final_data, team_away_stats, on=['AwayTeam'], how='outer')
    final_data = final_data.sort_values('Date',ascending=False)
    print(final_data)
    return final_data

def model_training(final_data):
    columns_to_predict = ['FTR_A', 'FTR_D', 'FTR_H']
    teams = ['HomeTeam','AwayTeam']
    X = final_data.drop(['Date'] + columns_to_predict, axis=1)
    y = final_data[columns_to_predict]
    onehotencoder = OneHotEncoder(drop='first', sparse_output=False)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = MultiOutputRegressor(LogisticRegression())
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, np.round(y_pred))  # Round predictions for comparison
    print("Accuracy Score:", accuracy)
    return accuracy


matches = load_df()
team_home_stats = get_20_10_5_home_last_matches(matches)
team_away_stats = get_20_10_5_away_last_matches(matches)
match_data = getting_matches_data()
final_data = merging_stats_to_match(team_home_stats, team_away_stats,match_data)
accuracy = model_training(final_data)


