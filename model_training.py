import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from functools import reduce
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import pickle

def load_df():
    last_season = pd.read_csv('data/B12324.csv')
    new_season = pd.read_csv('data/B12425.csv')
    df = pd.concat([last_season, new_season], axis=0)
    df.drop_duplicates(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.date
    df.sort_values('Date', ascending=False, inplace=True)
    matches = df[['Date','HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']]
    matches = matches.dropna()
    matches = pd.get_dummies(matches, columns=['FTR'])
    return matches

def get_10_5_3_home_last_matches(matches):
    last_home_10 = matches.groupby('HomeTeam').head(10)
    last_home_10.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_home_10 = last_home_10.drop(columns=['Date','AwayTeam'])
    last_home_10[['Loose', 'Draw', 'Win']] = last_home_10[['Loose', 'Draw', 'Win']].astype(int)
    last_home_10 = last_home_10.groupby('HomeTeam').mean()
    last_home_10 = last_home_10.add_suffix('_last_home_10')

    last_home_5 = matches.groupby('HomeTeam').head()
    last_home_5.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_home_5 = last_home_5.drop(columns=['Date','AwayTeam'])
    last_home_5[['Loose', 'Draw', 'Win']] = last_home_5[['Loose', 'Draw', 'Win']].astype(int)
    last_home_5 = last_home_5.groupby('HomeTeam').mean()
    last_home_5 = last_home_5.add_suffix('_last_home_5')

    last_home_3 = matches.groupby('HomeTeam').head(3)
    last_home_3.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_home_3 = last_home_3.drop(columns=['Date','AwayTeam'])
    last_home_3[['Loose', 'Draw', 'Win']] = last_home_3[['Loose', 'Draw', 'Win']].astype(int)
    last_home_3 = last_home_3.groupby('HomeTeam').mean()
    last_home_3 = last_home_3.add_suffix('_last_home_3')

    dfs = [last_home_10,last_home_5,last_home_3]
    team_home_stats = reduce(lambda left, right : pd.merge(left,right, on=['HomeTeam'],how='outer'), dfs)
    return team_home_stats

def get_10_5_3_away_last_matches(matches):
    last_away_10 = matches.groupby('AwayTeam').head(10)
    last_away_10.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_away_10 = last_away_10.drop(columns=['Date','HomeTeam'])
    last_away_10[['Loose', 'Draw', 'Win']] = last_away_10[['Loose', 'Draw', 'Win']].astype(int)
    last_away_10 = last_away_10.groupby('AwayTeam').mean()
    last_away_10 = last_away_10.add_suffix('_last_away_10')

    last_away_5 = matches.groupby('AwayTeam').head()
    last_away_5.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_away_5 = last_away_5.drop(columns=['Date','HomeTeam'])
    last_away_5[['Loose', 'Draw', 'Win']] = last_away_5[['Loose', 'Draw', 'Win']].astype(int)
    last_away_5 = last_away_5.groupby('AwayTeam').mean()
    last_away_5 = last_away_5.add_suffix('_last_away_5')

    last_away_3 = matches.groupby('AwayTeam').head(3)
    last_away_3.rename(columns={'FTR_A' : 'Loose', 'FTR_D' : 'Draw', 'FTR_H' : 'Win'}, inplace=True)
    last_away_3 = last_away_3.drop(columns=['Date','HomeTeam'])
    last_away_3[['Loose', 'Draw', 'Win']] = last_away_3[['Loose', 'Draw', 'Win']].astype(int)
    last_away_3 = last_away_3.groupby('AwayTeam').mean()
    last_away_3 = last_away_3.add_suffix('_last_away_3')

    dfs = [last_away_10,last_away_5,last_away_3]
    team_away_stats = reduce(lambda left, right : pd.merge(left,right, on=['AwayTeam'],how='outer'), dfs)
    return team_away_stats

def getting_matches_data():
    match_data = pd.read_csv('data/dataset.csv')
    match_data = match_data[['Date','HomeTeam','AwayTeam','FTR']]
    return match_data

def merging_stats_to_match(team_home_stats, team_away_stats, match_data):
    final_data = pd.merge(match_data, team_home_stats, on=['HomeTeam'], how='outer')
    final_data = pd.merge(final_data, team_away_stats, on=['AwayTeam'], how='outer')
    final_data = final_data.sort_values('Date',ascending=False)
    final_data = pd.get_dummies(final_data, columns=['FTR'])
    final_data = final_data.dropna()
    return final_data

def get_team_stats(team_home_stats, team_away_stats):
    team_away_stats = team_away_stats.reset_index()
    team_home_stats = team_home_stats.reset_index()
    team_away_stats.to_csv('data/team_away_stats.csv', index=False)
    team_home_stats.to_csv('data/team_home_stats.csv', index=False)
# Function to train the model with manual parameters
def model_training_with_manual_params(final_data, params):
    columns_to_predict = ['FTR_A', 'FTR_D', 'FTR_H']
    
    # OneHotEncode HomeTeam and AwayTeam
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False).set_output(transform="pandas")
    ohetransform = ohe.fit_transform(final_data[['HomeTeam', 'AwayTeam']])
    final_data = pd.concat([final_data, ohetransform], axis=1).drop(columns=['HomeTeam', 'AwayTeam'])
    with open ('utils/ohe.pkl', 'wb') as f:
        pickle.dump(ohe, f)
    
    X = final_data.drop(['Date'] + columns_to_predict, axis=1)
    y = final_data[columns_to_predict]
    
    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=233)
    
  
    # Initialize the LogisticRegression model with user-defined parameters
    params['random_state'] = 1
    model = MultiOutputClassifier(LogisticRegression(**params))
    
    # Fit the model to the training data
    model.fit(X_train, y_train)
    with open ('utils/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Calculate accuracy by comparing the predicted and true values
    y_pred_class = np.argmax(y_pred, axis=1)
    y_test_class = np.argmax(y_test.values, axis=1)
    accuracy = accuracy_score(y_test_class, y_pred_class)
    
    print("Accuracy Score with Manual Parameters:", accuracy)
    
    return accuracy

# Example usage of the function
matches = load_df()
team_home_stats = get_10_5_3_home_last_matches(matches)
team_away_stats = get_10_5_3_away_last_matches(matches)
team_stats = get_team_stats(team_home_stats, team_away_stats)
match_data = getting_matches_data()
final_data = merging_stats_to_match(team_home_stats, team_away_stats, match_data)
# Define manual parameters
manual_params = {
    'C': 1,  # Regularization strength
    'solver': 'liblinear',  # Solver to use
    'penalty': 'l2',  # Penalty type
    'max_iter': 500  # Number of iterations
}

# Train the model with manually selected parameters
accuracy = model_training_with_manual_params(final_data, manual_params)
