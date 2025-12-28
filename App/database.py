import sqlite3

dbName='ritomatchs.db'

def setup_db():
    with sqlite3.connect(dbName) as connection:
        cursor = connection.cursor()
        print("Database connected!")

        create_matchStats_query = '''CREATE TABLE IF NOT EXISTS match_stats(
        match_id TEXT PRIMARY KEY,
        summoner_name TEXT,
        champion TEXT,
        kills INTEGER,
        deaths INTEGER,
        assists INTEGER,
        win INTEGER,
        total_damage INTEGER,
        raw_json TEXT)'''

        cursor.execute(create_matchStats_query)
        print("Table 'match_stats' created sucessfully!")
        connection.commit()

def  add_match(match_id, name, champ, k, d, a, win, dmg, blob):
    with sqlite3.connect(dbName) as connection:
        cursor = connection.cursor()
        print("Database connected!")
    
        insert_matchStats_query= '''INSERT OR IGNORE INTO match_stats VALUES (
        ?,?,?,?,?,?,?,?,?)'''

        cursor.execute(insert_matchStats_query, (match_id, name, champ, k, d, a, win, dmg, blob))
        print(f"match {match_id} saved sucessfully!")
        connection.commit()
