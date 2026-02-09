import sqlite3

def setup_db(database):
    with sqlite3.connect(database) as connection:
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

def  add_match(database,match_id, summoner_name, champion, kills, deaths, assists, win, totaldamage, raw_json):
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        print("Database connected!")
    
        insert_matchStats_query= '''INSERT OR IGNORE INTO match_stats VALUES (
        ?,?,?,?,?,?,?,?,?)'''

        expectedData = (match_id, summoner_name, champion, kills, deaths, assists, win, totaldamage, raw_json)

        cursor.execute(insert_matchStats_query, expectedData)
        print(f"match {match_id} saved sucessfully!")
        connection.commit()
