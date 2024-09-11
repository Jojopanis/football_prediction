import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def show_predict():
    df = pd.read_csv("final_dataset.csv")

    team_names = {
        'St. Gilloise': 1, 'Club Brugge': 2, 'Dender': 3, 'Gent': 4, 'Antwerp': 5, 'Anderlecht': 6,
        'Genk': 7, 'Charleroi': 8, 'Mechelen': 9, 'Standard': 10, 'Oud-Heverlee Leuven': 11, 'Westerlo': 12,
        'Cercle Brugge': 13, 'St Truiden': 14, 'Mouscron': 15, 'Waregem': 16, 'Kortrijk': 17, 'Oostende': 18,
        'Eupen': 19, 'Beerschot VA': 20, 'RWD Molenbeek': 21, 'Waasland-Beveren': 22, 'Seraing': 23
    }

    le_home = LabelEncoder()
    le_away = LabelEncoder()
    df['HomeTeamEncoded'] = le_home.fit_transform(df['HomeTeam'])
    df['AwayTeamEncoded'] = le_away.fit_transform(df['AwayTeam'])

    feature_columns = ['HomeTeamEncoded', 'AwayTeamEncoded']
    target_columns = ['FTHG', 'FTAG']

    X = df[feature_columns]
    y = df[target_columns]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    multi_output_model = MultiOutputRegressor(model)
    multi_output_model.fit(X_train, y_train)

    st.write("### Predict the Match Result")
    home_team = st.selectbox("Home Team", list(team_names.keys()))
    away_team = st.selectbox("Away Team", list(team_names.keys()))

    home_team_encoded = team_names[home_team]
    away_team_encoded = team_names[away_team]

    input_data = pd.DataFrame({
        'HomeTeamEncoded': [home_team_encoded],
        'AwayTeamEncoded': [away_team_encoded]
    })

    if st.button("Predict"):
        prediction = multi_output_model.predict(input_data)
        home_score = round(prediction[0][0])
        away_score = round(prediction[0][1])
        
        st.write(f"**{home_team} Goals:** {home_score}")
        st.write(f"**{away_team} Goals:** {away_score}")

  
