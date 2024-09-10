from bs4 import BeautifulSoup
import pandas as pd
import requests
import sqlite3
from csv_processing import populate_tables, get_csv

url = "https://www.walfoot.be/belgique/jupiler-pro-league/calendrier"

text = requests.get(f"{url}",headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
soup = BeautifulSoup(text.text,features="html.parser")

table = soup.find_all("table")
df = pd.read_html(str(table))[0]
df = df.iloc[1:,:-1]
df.columns = ['date', 'home', 'score', 'away']
df['date'] = df['date'].apply(lambda x: x.split(" ")[0])

def add_year(date:str):
    if int(date.split("/")[1]) < 7:
        return f"{date}/2025"
    else:
        return f"{date}/2024"
    
df['date'] = df['date'].apply(add_year)
df['home'].sort_values().unique()

def change_team_names(name:str):
    names_dict = {
        "Anderlecht":"Anderlecht",
        "Antwerp":"Antwerp",
        "Beerschot":"Beerschot VA",
        "Cercle de Bruges":"Cercle Brugge",
        "Charleroi":"Charleroi",
        "FC Bruges":"Club Brugge",
        "FCV Dender EH":"Dender",
        "KRC Genk":"Genk",
        "La Gantoise":"Gent",
        "KV Courtrai":"Kortrijk",
        "KV Malines":"Mechelen",
        "OH Louvain":"Leuven",
        "STVV":"St Truiden",
        "Union SG":"St. Gilloise",
        "Standard":"Standard",
        "Westerlo":"Westerlo"
    }
    for key, value in names_dict.items():
        if key in name:
            return value
        
df['home'] = df['home'].apply(change_team_names)
df['away'] = df['away'].apply(change_team_names)

df.drop(df[df['score'].str[0] != "."].index,inplace=True)
df.drop('score', axis = 1, inplace = True)
df.columns = ['Date','HomeTeam','AwayTeam']

df.to_csv("data/future_matches.csv",index=False)

matches = get_csv("data/future_matches.csv")
db = sqlite3.connect('data/JupilerProLeague.db')
populate_tables(matches)