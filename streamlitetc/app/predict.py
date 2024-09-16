import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import sqlite3
import os

def show_predict():
    df = pd.read_csv("final_dataset.csv")

    team_names = {
        'Anderlecht': 15.5, 'Dender': 12.833333333333334, 'Genk': 12.700000000000001, 'Oud-Heverlee Leuven': 12.0,
        'Club Brugge': 10.75, 'Westerlo': 10.75, 'St. Gilloise': 9.75, 'Gent': 8.7, 'Charleroi': 8.166666666666666,
        'Mechelen': 7.833333333333334, 'Antwerp': 7.249999999999998, 'Standard': 6.833333333333334, 
        'Kortrijk': 4.916666666666667, 'Cercle Brugge': 2.0, 'St Truiden': -1.0, 'Beerschot VA': -3.666666666666666
    }

    code_to_team = {v: k for k, v in team_names.items()}

    feature_columns = ['HomeTeamEncoded', 'AwayTeamEncoded', 'HTHG', 'HTAG', 'FTR', 'HTR' , 'HS', 'AS',
                       'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR']
    target_columns = ['FTHG', 'FTAG']

    le_home = LabelEncoder()
    le_away = LabelEncoder()    
    df['HomeTeamEncoded'] = le_home.fit_transform(df['HomeTeam'])
    df['AwayTeamEncoded'] = le_away.fit_transform(df['AwayTeam'])

    X = df[feature_columns]
    y = df[target_columns]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestRegressor(n_estimators=200, max_depth=7 ,max_features='sqrt' , min_samples_leaf=1, min_samples_split=2)
    multi_output_model = MultiOutputRegressor(model)
    multi_output_model.fit(X_train, y_train)

    st.write("<h3 style='font-size:48px;'>Match Prediction</h3>", unsafe_allow_html=True)

    team_logo = {
        'Anderlecht': 'logos/Anderlecht.png', 
        'Dender': 'logos/Dender.png', 
        'Genk': 'logos/Genk.png',
        'Oud-Heverlee Leuven': 'logos/Oud-Heverlee Leuven.png', 
        'Club Brugge': 'logos/Club Brugge.png',
        'Westerlo': 'logos/Westerlo.png',
        'St. Gilloise': 'logos/St. Gilloise.png', 
        'Gent': 'logos/Gent.png', 
        'Charleroi': 'logos/Charleroi.png',
        'Mechelen': 'logos/Mechelen.png',
        'Antwerp': 'logos/Antwerp.png', 
        'Standard': 'logos/Standard.png',
        'Kortrijk': 'logos/Kortrijk.png', 
        'Cercle Brugge': 'logos/Cercle-Brugge.png', 
        'St Truiden': 'logos/St Truiden.png', 
        'Beerschot VA': 'logos/Beerschot VA.png'
    }

    col1, col2 = st.columns(2)

    with col1:
        home_team = st.selectbox("Home Team", list(team_names.keys()), key='home_team_selector')
        logo_path_home = team_logo.get(home_team, None)
        if logo_path_home and os.path.isfile(logo_path_home):
            st.image(logo_path_home, width=60)
        else:
            st.write(f"Logo not found for {home_team}")

    with col2:
        away_team = st.selectbox("Away Team", list(team_names.keys()), key='away_team_selector')
        logo_path_away = team_logo.get(away_team, None)
        if logo_path_away and os.path.isfile(logo_path_away):
            st.image(logo_path_away, width=60)
        else:
            st.write(f"Logo not found for {away_team}")

    home_team_encoded = team_names[home_team]
    away_team_encoded = team_names[away_team]

    default_values = {
        'HTHG': 0, 'HTAG': 0, 'FTR': 0, 'HTR': 0, 'HS': 10, 'AS': 10,
        'HST': 5, 'AST': 5, 'HF': 10, 'AF': 10, 'HC': 4, 'AC': 4,
        'HY': 1, 'AY': 1, 'HR': 0, 'AR': 0
    }

    input_data = pd.DataFrame({
        'HomeTeamEncoded': [home_team_encoded],
        'AwayTeamEncoded': [away_team_encoded],
        'HTHG': [default_values['HTHG']],
        'HTAG': [default_values['HTAG']],
        'FTR': [default_values['FTR']],
        'HTR': [default_values['HTR']],
        'HS': [default_values['HS']],
        'AS': [default_values['AS']],
        'HST': [default_values['HST']],
        'AST': [default_values['AST']],
        'HF': [default_values['HF']],
        'AF': [default_values['AF']],
        'HC': [default_values['HC']],
        'AC': [default_values['AC']],
        'HY': [default_values['HY']],
        'AY': [default_values['AY']],
        'HR': [default_values['HR']],
        'AR': [default_values['AR']]
    })

    conn = sqlite3.connect('data/JupilerProLeague.db')
    
    query = f"""
    SELECT 
        HomeTeam, AwayTeam, FTHG, FTAG, Date
    FROM 
        matches
    WHERE 
        (HomeTeam = {home_team_encoded} AND AwayTeam = {away_team_encoded}) 
        OR 
        (HomeTeam = {away_team_encoded} AND AwayTeam = {home_team_encoded})
    ORDER BY 
        Date DESC  
    LIMIT 5
    """
    
    try:
        past_matches = pd.read_sql(query, conn)
        
        past_matches['HomeTeam'] = past_matches['HomeTeam'].map(code_to_team)
        past_matches['AwayTeam'] = past_matches['AwayTeam'].map(code_to_team)
        
        st.write("<h3 style='font-size:24px;'>Last 5 Matches</h3>", unsafe_allow_html=True)
        st.write(past_matches)
    except Exception as e:
        st.write(f"Error: {e}")
    finally:
        conn.close()

    if st.button("Predict"):
        prediction = multi_output_model.predict(input_data)
        
        home_score = round(prediction[0][0])
        away_score = round(prediction[0][1])
        
        st.write(f"**{home_team} Goals:** {home_score}") 
        st.write(f"**{away_team} Goals:** {away_score}")
