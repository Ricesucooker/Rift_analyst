import duckdb
 
#'ritomatchs.db' database 

class MatchAnalyst:
    def __init__(self, db_path):
        self.dbName = db_path
        self.con =duckdb.connect()
        self.con.execute("Install sqlite")
        self.con.execute("Load sqlite")
        self.con.execute(f"ATTACH '{self.dbName}' as database (Type sqlite, READ_ONLY 1);")

        # #in-memoeryDatabase 
        # def viewGames():
        #     with duckdb.connect() as connection:
        #         connection.execute("Install sqlite")
        #         connection.execute("Load sqlite")
        #         connection.execute(f"ATTACH '{dbName}' as database (Type sqlite, READ_ONLY 1)")
        #         connection.sql("Select * from database.match_stats limit 10").show()


        # def top3KDAgame():
        #     with duckdb.connect() as connection:
        #         connection.execute("Install sqlite")
        #         connection.execute("Load sqlite")
        #         connection.execute(f"ATTACH '{dbName}' as database (Type sqlite, READ_ONLY 1)")
        #         connection.sql("Select any_value(match_id) as Game,champion, round(AVG((kills+assists)/cast(deaths+1 as float)),2) as Avg_KDA from database.match_stats group by champion order by AVG_KDA DESC LIMIT 3").show()

        # print("Last 10 game play")
        # viewGames()
        # print ("Top 3 KDA Games and history")
        # top3KDAgame()

    def view_recent_games(self, limit_num=10):
        print(f"\n-- Last {limit_num} Games ---")
        self.con.sql(f"select * from database.match_stats limit {limit_num}").show()

    def get_best_champion_KDA(self):
        print(f"\n--- Top Champion KDA ---")
        query = """ 
                Select any_value(match_id) as Game,
                        champion,
                        Round(AVG((kills+assists)/cast(deaths+1 as float)),2) as Avarage_KDA
                        from database.match_stats 
                        group by champion
                        order by Avarage_KDA desc"""
        self.con.sql(query).show()