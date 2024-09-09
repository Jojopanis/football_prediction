from utils.csv_processing import create_tables, populate_tables, process_csv
import sqlite3

db = sqlite3.connect('data/JupilerProLeague.db')

if __name__ == '__main__':
    create_tables(db)
    matches, stats = process_csv('data/B12324.csv')
    populate_tables(matches, stats)