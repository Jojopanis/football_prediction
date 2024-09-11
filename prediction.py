import pickle
import pandas as pd
import numpy as np

model = pickle.load(open('data/model.pkl', 'rb'))
ohe = pickle.load(open('data/ohe.pkl', 'rb'))

futur_matches = pd.read_csv('data/future_matches.csv')
team_home_stats = pd.read_csv('data/team_home_stats.csv')
team_home_stats = team_home_stats.drop(team_home_stats[team_home_stats['HomeTeam'] == 'Eupen'].index)
team_home_stats = team_home_stats.drop(team_home_stats[team_home_stats['HomeTeam'] == 'RWD Molenbeek'].index)
team_away_stats = pd.read_csv('data/team_away_stats.csv')
team_away_stats = team_away_stats.drop(team_away_stats[team_away_stats['AwayTeam'] == 'Eupen'].index)
team_away_stats = team_away_stats.drop(team_away_stats[team_away_stats['AwayTeam'] == 'RWD Molenbeek'].index)

futur_matches.rename(columns={'Home': 'HomeTeam', 'Away': 'AwayTeam'}, inplace=True)
futur_matches = pd.merge(futur_matches, team_home_stats, on=['HomeTeam'], how='outer')
futur_matches_stats = pd.merge(futur_matches, team_away_stats, on=['AwayTeam'], how='outer')

futur_matches_stats['match_id'] = futur_matches_stats.index # Create a match_id to ensure alignment

futur_matches_stats['Date'] = pd.to_datetime(futur_matches_stats['Date'], format='%d/%m/%Y').dt.date
futur_matches_stats.sort_values('Date', ascending=True, inplace=True)

matches = futur_matches_stats[['Date', 'HomeTeam', 'AwayTeam', 'match_id']]  # Include the match_id to ensure alignment

ohetransform = ohe.transform(futur_matches_stats[['HomeTeam', 'AwayTeam']])

prediction = pd.concat([futur_matches_stats, ohetransform], axis=1).drop(['HomeTeam', 'AwayTeam'], axis=1)

prediction.dropna(inplace=True)

X = prediction.drop(['Date', 'match_id'], axis=1)  # Drop Date and match_id from features

y = model.predict(X)
proba = model.predict_proba(X)
proba = proba[0]  # Extract the probabilities for the first match only
proba = proba * 100 # Convert the probabilities to percentages
proba = np.round(proba, 2)  # Round the probabilities to two decimal places
y = pd.DataFrame(y, columns=['Prediction'])
proba = pd.DataFrame(proba, columns=['FTR_A','FTR_D','FTR_H'])

results = pd.concat([proba, y], axis=1)
results['match_id'] = prediction['match_id'].values  # Add match_id to results

merged_results = pd.merge(matches, results, on='match_id', how='left')

merged_results.drop('match_id', axis=1, inplace=True)

merged_results.to_csv('data/predictions.csv', index=False)