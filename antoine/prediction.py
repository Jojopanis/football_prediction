import pickle
import pandas as pd
import numpy as np

def predict_future_matches(model_path, ohe_path, future_matches_path, home_stats_path, away_stats_path, output_path):
    # Load model and encoder
    model = pickle.load(open(model_path, 'rb'))
    ohe = pickle.load(open(ohe_path, 'rb'))
    
    # Load data
    future_matches = pd.read_csv(future_matches_path)
    team_home_stats = pd.read_csv(home_stats_path)
    team_away_stats = pd.read_csv(away_stats_path)

    # Drop specific teams from home and away stats
    team_home_stats = team_home_stats.drop(team_home_stats[team_home_stats['HomeTeam'] == 'Eupen'].index)
    team_home_stats = team_home_stats.drop(team_home_stats[team_home_stats['HomeTeam'] == 'RWD Molenbeek'].index)
    team_away_stats = team_away_stats.drop(team_away_stats[team_away_stats['AwayTeam'] == 'Eupen'].index)
    team_away_stats = team_away_stats.drop(team_away_stats[team_away_stats['AwayTeam'] == 'RWD Molenbeek'].index)

    # Prepare future matches data
    future_matches.rename(columns={'Home': 'HomeTeam', 'Away': 'AwayTeam'}, inplace=True)
    future_matches = pd.merge(future_matches, team_home_stats, on=['HomeTeam'], how='outer')
    future_matches_stats = pd.merge(future_matches, team_away_stats, on=['AwayTeam'], how='outer')

    # Create match_id and sort by date
    future_matches_stats['match_id'] = future_matches_stats.index
    future_matches_stats['Date'] = pd.to_datetime(future_matches_stats['Date'], format='%d/%m/%Y').dt.date
    future_matches_stats.sort_values('Date', ascending=True, inplace=True)

    # Prepare match data
    matches = future_matches_stats[['Date', 'HomeTeam', 'AwayTeam', 'match_id']]

    # One-hot encoding
    ohe_transform = ohe.transform(future_matches_stats[['HomeTeam', 'AwayTeam']])

    # Concatenate and clean up
    prediction = pd.concat([future_matches_stats, ohe_transform], axis=1).drop(['HomeTeam', 'AwayTeam'], axis=1)
    prediction.dropna(inplace=True)

    # Prepare feature matrix
    X = prediction.drop(['Date', 'match_id'], axis=1)

    # Model prediction
    y = model.predict(X)
    proba = model.predict_proba(X)[0]  # Extract probabilities for the first match only
    proba = np.round(proba * 100, 2)   # Convert to percentage and round

    # Prepare results
    y_df = pd.DataFrame(y, columns=['Prediction'])
    proba_df = pd.DataFrame(proba, columns=['FTR_A', 'FTR_D', 'FTR_H'])
    results = pd.concat([proba_df, y_df], axis=1)
    results['match_id'] = prediction['match_id'].values

    # Merge results with match info
    merged_results = pd.merge(matches, results, on='match_id', how='left')
    merged_results.drop('match_id', axis=1, inplace=True)

    # Save results
    merged_results.to_csv(output_path, index=False)

    print("Predictions saved to", output_path)

predict_future_matches('data/model.pkl', 'data/ohe.pkl', 'data/future_matches.csv', 
                       'data/team_home_stats.csv', 'data/team_away_stats.csv', 'data/predictions.csv')
