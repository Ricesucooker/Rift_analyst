import duckdb
 
#'ritomatchs.db' database 

class MatchAnalyst:
    """
    Docstring for MatchAnalyst
    :param
        Database connection and load sqllite for read only.
    """
    def __init__(self, db_path):
        self.dbName = db_path
        self.con =duckdb.connect()
        self.con.execute("Install sqlite")
        self.con.execute("Load sqlite")
        self.con.execute(f"ATTACH '{self.dbName}' as database (Type sqlite, READ_ONLY 1);")


    def view_recent_games(self, limit_num=10):
        """
        view_recent_games
        :param self: self query recent games 
        :param limit_num: limit default 10 
        """
        print(f"\n-- Last {limit_num} Games ---")
        self.con.sql(f"select * from database.match_stats limit {limit_num}").show()

    def get_best_champion_KDA(self):
        """
        get_best_champion_KDA
        :param self: Self query avarage KDA
        """
        print(f"\n--- Top Champion KDA ---")
        query = """ 
                Select any_value(match_id) as Game,
                        champion,
                        Round(AVG((kills+assists)/cast(deaths+1 as float)),2) as Avarage_KDA
                        from database.match_stats 
                        group by champion
                        order by Avarage_KDA desc limit 5"""
        self.con.sql(query).show()