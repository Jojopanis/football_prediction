import pandas as pd
import sqlite3

db = sqlite3.connect('db/JupilerProLeague.db')

def read_csv(file_path:str='db/dataset.csv'): 
    df = pd.read_csv(file_path)
    matches = df[['Date','HomeTeam','AwayTeam']]
    matches.columns = ['date','home','away']
    stats = df[['FTHG','FTAG','FTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
    stats.columns = ['full_time_home_goals','full_time_away_goals','full_time_result','home_shots','away_shots','home_shots_target','away_shots_target','home_fouls','away_fouls','home_corners','away_corners','home_yellow','away_yellow','home_red','away_red']
    return matches, stats

def create_tables():
    sql_statements = [
        '''CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
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

def populate_tables(matches:pd.DataFrame, stats:pd.DataFrame):

    with db as conn:
        cursor = conn.cursor()

        cursor.executemany('''
        INSERT INTO matches (date, home, away)
        VALUES (?, ?, ?)''', 
        matches.values.tolist())
        
        cursor.execute('SELECT last_insert_rowid()')
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

if __name__ == '__main__':
    matches, stats = read_csv()
    create_tables()
    populate_tables(matches, stats)