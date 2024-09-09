import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from functools import reduce


pd.options.display.float_format = "{:,.2f}".format


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
    last_home_20.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win', 'HomeTeam' : 'Team'}, inplace=True)
    last_home_20 = last_home_20.drop(columns=['Date','AwayTeam'])
    last_home_20[['Loose', 'Draw', 'Win']] = last_home_20[['Loose', 'Draw', 'Win']].astype(int)
    last_home_20 = last_home_20.groupby('Team').mean()
    last_home_20 = last_home_20.add_suffix('_last_home_20')
# Getting the 10 lasts games played at home for each team
    last_home_10 = matches.groupby('HomeTeam').head(10)
    last_home_10.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win', 'HomeTeam' : 'Team'}, inplace=True)
    last_home_10 = last_home_10.drop(columns=['Date','AwayTeam'])
    last_home_10[['Loose', 'Draw', 'Win']] = last_home_10[['Loose', 'Draw', 'Win']].astype(int)
    last_home_10 = last_home_10.groupby('Team').mean()
    last_home_10 = last_home_10.add_suffix('_last_home_10')
# Getting the 20 lasts games played at home for each team
    last_home_5 = matches.groupby('HomeTeam').head()
    last_home_5.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win', 'HomeTeam' : 'Team'}, inplace=True)
    last_home_5 = last_home_5.drop(columns=['Date','AwayTeam'])
    last_home_5[['Loose', 'Draw', 'Win']] = last_home_5[['Loose', 'Draw', 'Win']].astype(int)
    last_home_5 = last_home_5.groupby('Team').mean()
    last_home_5 = last_home_5.add_suffix('_last_home_5')
# Merging all the df into a single one   
    dfs = [last_home_20,last_home_10,last_home_5]
    team_home_stats = reduce(lambda left, right : pd.merge(left,right, on=['Team'],how='outer'), dfs)
    return team_home_stats


def get_20_10_5_away_last_matches(matches):
# Getting the 20 lasts games played away for each team
    last_away_20 = matches.groupby('AwayTeam').head(20)
    last_away_20.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win', 'HomeTeam' : 'Team'}, inplace=True)
    last_away_20 = last_away_20.drop(columns=['Date','AwayTeam'])
    last_away_20[['Loose', 'Draw', 'Win']] = last_away_20[['Loose', 'Draw', 'Win']].astype(int)
    last_away_20 = last_away_20.groupby('Team').mean()
    last_away_20 = last_away_20.add_suffix('_last_away_20')
# Getting the 10 lasts games played away for each team
    last_away_10 = matches.groupby('HomeTeam').head(10)
    last_away_10.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win', 'HomeTeam' : 'Team'}, inplace=True)
    last_away_10 = last_away_10.drop(columns=['Date','AwayTeam'])
    last_away_10[['Loose', 'Draw', 'Win']] = last_away_10[['Loose', 'Draw', 'Win']].astype(int)
    last_away_10 = last_away_10.groupby('Team').mean()
    last_away_10 = last_away_10.add_suffix('_last_away_10')
# Getting the 5 lasts games played away for each team
    last_away_5 = matches.groupby('HomeTeam').head()
    last_away_5.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win', 'HomeTeam' : 'Team'}, inplace=True)
    last_away_5 = last_away_5.drop(columns=['Date','AwayTeam'])
    last_away_5[['Loose', 'Draw', 'Win']] = last_away_5[['Loose', 'Draw', 'Win']].astype(int)
    last_away_5 = last_away_5.groupby('Team').mean()
    last_away_5 = last_away_5.add_suffix('_last_away_5')
# Merging all the df into a single one   
    dfs = [last_away_20,last_away_10,last_away_5]
    team_away_stats = reduce(lambda left, right : pd.merge(left,right, on=['Team'],how='outer'), dfs)
    return team_away_stats

def get_a_single_df(team_home_stats, team_away_stats):
    team_stats = pd.merge(team_away_stats, team_home_stats, on=['Team'],how='outer')
    print(team_stats)
    return team_stats

matches = load_df()
team_home_stats = get_20_10_5_home_last_matches(matches)
team_away_stats = get_20_10_5_away_last_matches(matches)
team_stats = get_a_single_df(team_home_stats,team_away_stats)
team_stats.to_csv("db/team_stats.csv")