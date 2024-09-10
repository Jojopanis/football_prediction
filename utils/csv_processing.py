import pandas as pd
import sqlite3
import datetime

db = sqlite3.connect('data/JupilerProLeague.db')

def get_csv(file_path:str): 
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.date
    df.sort_values(by='Date', inplace=True)
    return df
    
def split_csv(df:pd.DataFrame):
    matches = df[['Date','HomeTeam','AwayTeam']]
    matches.columns = ['date','home','away']
    stats = df[['FTHG','FTAG','FTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
    stats.columns = ['full_time_home_goals','full_time_away_goals','full_time_result','home_shots','away_shots','home_shots_target','away_shots_target','home_fouls','away_fouls','home_corners','away_corners','home_yellow','away_yellow','home_red','away_red']
    return matches, stats

def create_tables(db:sqlite3.Connection):
    sql_statements = [
        '''CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                date DATE NOT NULL,
                home TEXT NOT NULL,
                away TEXT NOT NULL
        )''',
        '''CREATE TABLE IF NOT EXISTS stats (
                id INTEGER PRIMARY KEY,
                match_id INTEGER NOT NULL,
                full_time_home_goals INTEGER NOT NULL,
                full_time_away_goals INTEGER NOT NULL,
                full_time_result TEXT NOT NULL,
                home_shots INTEGER,
                away_shots INTEGER,
                home_shots_target INTEGER,
                away_shots_target INTEGER,
                home_fouls INTEGER,
                away_fouls INTEGER,
                home_corners INTEGER,
                away_corners INTEGER,
                home_yellow INTEGER,
                away_yellow INTEGER,
                home_red INTEGER,
                away_red INTEGER,
                FOREIGN KEY (match_id) REFERENCES matches(id)
        )''']
    
    with db as conn:
        cursor = conn.cursor()
        for sql in sql_statements:
            cursor.execute(sql)
        conn.commit()

def populate_tables(matches:pd.DataFrame, stats:pd.DataFrame=None):

    with db as conn:
        cursor = conn.cursor()

        cursor.executemany('''
        INSERT INTO matches (date, home, away)
        VALUES (?, ?, ?)''', 
        matches.values.tolist())
        
        cursor.execute('SELECT last_insert_rowid()')

        if stats is not None:
            last_id = cursor.fetchone()[0]
            match_ids = list(range(last_id - len(matches) + 1, last_id + 1))

            stats['match_id'] = match_ids
            stats = stats[['match_id','full_time_home_goals','full_time_away_goals','full_time_result','home_shots','away_shots','home_shots_target','away_shots_target','home_fouls','away_fouls','home_corners','away_corners','home_yellow','away_yellow','home_red','away_red']]

            cursor.executemany('''
            INSERT INTO stats (match_id, full_time_home_goals, full_time_away_goals, full_time_result, 
                                home_shots, away_shots, home_shots_target, away_shots_target,
                                home_fouls, away_fouls, home_corners, away_corners,
                                home_yellow, away_yellow, home_red, away_red)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            stats.values.tolist())

def prune_csv(df:pd.DataFrame):
    with db as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date FROM matches ORDER BY date DESC LIMIT 1')
        last_weekend = cursor.fetchone()
    if last_weekend is not None:
        df = df[df['Date'] > datetime.datetime.strptime(last_weekend[0], "%Y-%m-%d").date()]
    return df

def process_csv(file_path:str):
    df = get_csv(file_path)
    df = prune_csv(df)
    matches, stats = split_csv(df)
    return matches, stats

if __name__ == '__main__':
    create_tables()
    matches, stats = process_csv('data/B1.csv')
    populate_tables(matches, stats)