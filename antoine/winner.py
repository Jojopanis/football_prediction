import pandas as pd
import numpy as np 
import pickle

already_passed_match = pd.read_csv('data/B12425.csv')
prediction = pd.read_csv('data/predictions.csv')

Predi_Home_points = []
Predi_Away_points = []

for index, row in prediction.iterrows():
    if row['Prediction'] == 'FTR_H':
        Predi_Home_points.append(3)
        Predi_Away_points.append(0)
    elif row['Prediction'] == 'FTR_A':
        Predi_Home_points.append(0)
        Predi_Away_points.append(3)
    else:
        Predi_Home_points.append(1)
        Predi_Away_points.append(1)

prediction['Home_points'] = Predi_Home_points
prediction['Away_points'] = Predi_Away_points
prediction

predi_teams_home_point = prediction.groupby('HomeTeam')['Home_points'].sum()
predi_teams_away_point = prediction.groupby('AwayTeam')['Away_points'].sum()
predi_teams_point = predi_teams_home_point.add(predi_teams_away_point, fill_value=0)
predi_teams_point.sort_values(ascending=False, inplace=True)
predi_teams_point


home_points = []
away_points = []

for index, row in already_passed_match.iterrows():
    if row['FTR'] == 'H':
        home_points.append(3)
        away_points.append(0)
    elif row['FTR'] == 'A':
        home_points.append(0)
        away_points.append(3)
    else:
        home_points.append(1)
        away_points.append(1)

already_passed_match['Home_points'] = home_points
already_passed_match['Away_points'] = away_points
teams_home_point = already_passed_match.groupby('HomeTeam')['Home_points'].sum()
teams_away_point = already_passed_match.groupby('AwayTeam')['Away_points'].sum()
teams_point = teams_home_point.add(teams_away_point, fill_value=0)
teams_point.sort_values(ascending=False, inplace=True)
teams_point = teams_point.add(predi_teams_point, fill_value=0)
teams_point.sort_values(ascending=False, inplace=True)
teams_point = pd.DataFrame(teams_point)
teams_point.rename(columns={0: 'Points'}, inplace=True)
teams_point.reset_index(inplace=True)
play_off_teams = teams_point.head(6)
play_off_teams['Points'] = (play_off_teams['Points'].astype(int) / 2).round(0)

model = pickle.load(open('data/model.pkl', 'rb'))
ohe = pickle.load(open('data/ohe.pkl', 'rb'))

play_off_matches = []
for i in range(len(play_off_teams)):
    for j in range(len(play_off_teams)):
        if i != j:
            play_off_matches.append([play_off_teams.iloc[i]['HomeTeam'], play_off_teams.iloc[j]['HomeTeam']])

play_off_matches = pd.DataFrame(play_off_matches, columns=['HomeTeam', 'AwayTeam'])
play_off_matches


home_stats = pd.read_csv('data/team_home_stats.csv')
away_stats = pd.read_csv('data/team_away_stats.csv')

play_off_matches = pd.merge(play_off_matches, home_stats, on='HomeTeam', how='left')
play_off_matches = pd.merge(play_off_matches, away_stats, on='AwayTeam', how='left')
play_off_matches

ohetransform = ohe.transform(play_off_matches[['HomeTeam', 'AwayTeam']])
play_off_matches_encoded = pd.concat([play_off_matches, ohetransform], axis=1).drop(['HomeTeam', 'AwayTeam'], axis=1)
play_off_matches_encoded.dropna(inplace=True)

X = play_off_matches_encoded
y = model.predict(X)
proba = model.predict_proba(X)
proba = np.round(proba, 2)
proba = proba[0]
y = pd.DataFrame(y, columns=['Prediction'])
proba = pd.DataFrame(proba, columns=['FTR_A','FTR_D','FTR_H'])
results = pd.concat([proba, y], axis=1)

results['HomeTeam'] = play_off_matches['HomeTeam']
results['AwayTeam'] = play_off_matches['AwayTeam']

home_points_pred = []
away_points_pred = []

for index, row in results.iterrows():
    if row['Prediction'] == 'FTR_H':
        home_points_pred.append(3)
        away_points_pred.append(0)
    elif row['Prediction'] == 'FTR_A':
        home_points_pred.append(0)
        away_points_pred.append(3)
    else:
        home_points_pred.append(1)
        away_points_pred.append(1)


results['Home_points'] = home_points_pred
results['Away_points'] = away_points_pred
results_home = results.groupby('HomeTeam')['Home_points'].sum()
results_away = results.groupby('AwayTeam')['Away_points'].sum()
results_points = results_home.add(results_away, fill_value=0)
results_points.sort_values(ascending=False, inplace=True)
results_points = pd.DataFrame(results_points)
results_points.rename(columns={0: 'Points'}, inplace=True)
results_points.reset_index(inplace=True)
winner = pd.concat([play_off_teams, results_points], axis=0)
winner = winner.groupby('HomeTeam')['Points'].sum()
winner.sort_values(ascending=False, inplace=True)
winner = pd.DataFrame(winner)
championship_leaders = winner.head(3)
championship_leaders.to_csv('data/championship_leaders.csv')
