import duckdb

dbName='ritomatchs.db'



#in-memoeryDatabase 
def viewGames():
    with duckdb.connect() as connection:
        connection.execute("Install sqlite")
        connection.execute("Load sqlite")
        connection.execute(f"ATTACH '{dbName}' as database (Type sqlite, READ_ONLY 1)")
        connection.sql("Select * from database.match_stats limit 10").show()


def top3KDAgame():
    with duckdb.connect() as connection:
        connection.execute("Install sqlite")
        connection.execute("Load sqlite")
        connection.execute(f"ATTACH '{dbName}' as database (Type sqlite, READ_ONLY 1)")
        connection.sql("Select any_value(match_id) as Game,champion, round(AVG((kills+assists)/cast(deaths+1 as float)),2) as Avg_KDA from database.match_stats group by champion order by AVG_KDA DESC LIMIT 3").show()




print("Last 10 game play")
viewGames()
print ("Top 3 KDA Games and history")
top3KDAgame()