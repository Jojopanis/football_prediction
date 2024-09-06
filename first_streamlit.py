import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import OneHotEncoder



# Load data 

df = pd.read_csv('dataset.csv')
df = df[['Date' , 'HomeTeam','AwayTeam','FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
df= pd.get_dummies(df, columns=['FTR','HTR'])
matches = df.groupby(['HomeTeam','AwayTeam'])[['FTR_A','FTR_D','FTR_H','HTR_A','HTR_D','HTR_H']].sum().reset_index()
matches_stats = df.groupby(['HomeTeam','AwayTeam'])[['FTHG','FTAG','HTHG','HTAG','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']].mean().reset_index()
matches = pd.merge(matches, matches_stats, on=['HomeTeam','AwayTeam'])
matches['total_matches'] = matches['FTR_A'] + matches['FTR_D'] + matches['FTR_H']

st.title('Football Match Prediction')

home_team = st.selectbox('Select Home Team', matches['HomeTeam'].unique())
away_team = st.selectbox('Select Away Team', matches['AwayTeam'].unique())

if home_team == away_team:
    st.error('Please select different teams')
else:
    None

home_team_stats = matches[matches['HomeTeam'] == home_team]
away_team_stats = matches[matches['AwayTeam'] == away_team]

if st.button('Predict match result'):
    match_stats = matches[(matches['HomeTeam'] == home_team) & (matches['AwayTeam'] == away_team)]
    
    if not match_stats.empty:
        total_matches_between_teams = match_stats['total_matches'].values[0]
        home_team_win = match_stats['FTR_H'].values[0] / total_matches_between_teams
        away_team_win = match_stats['FTR_A'].values[0] / total_matches_between_teams
        draw = match_stats['FTR_D'].values[0] / total_matches_between_teams
        
        st.subheader('Win, draw, lose probabilities') 
        st.write(f'{home_team} win probability: {home_team_win:.2f}')
        st.write(f'{away_team} win probability: {away_team_win:.2f}')
        st.write(f'Draw probability: {draw:.2f}')

        st.subheader('bookmakers best possible odds') 
        st.write(f'{home_team} win odds: {1/home_team_win:.2f}')
        st.write(f'{away_team} win odds: {1/away_team_win:.2f}')
        st.write(f'Draw odds: {1/draw:.2f}')

        fig = go.Figure(data=[go.Pie(labels=[home_team, away_team, 'Draw'], 
                                     values=[home_team_win, away_team_win, draw])])
        st.plotly_chart(fig)
    else:
        st.write('No match data available between the selected teams.')


