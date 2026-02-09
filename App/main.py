from duckdb_analytics import MatchAnalyst
from engine import MatchEngine
from pathlib import Path #to do security 


class LOLMatchTrackerApp:
    def __init__(self,database,):
        self.database = database
        self.scriptLogic = MatchEngine(self.database)
        self.gameTracker = MatchAnalyst(self.database)
    
    def run(self):
        
        gameName = input("Summoners name : ")
        gameTag = input("# Tag : ")

        if not self.scriptLogic.setup_user(gameName,gameTag):
            print("Account not found. Exiting")
            return
        
        while True:
            modePicker = input("Please type [draft], [solo] or [flex] for the game mode data you are looking to pull:\n") .lower().strip()
            if self.scriptLogic.set_gamemode(modePicker) != False:
                break
        
        print("Gathering Data...")
        self.scriptLogic.get_match_list()
        self.scriptLogic.get_matchdata()

        print("\n--- Analytics Reports ----")
        self.gameTracker.view_recent_games()
        self.gameTracker.get_best_champion_KDA()


if __name__ == "__main__":
    
    app = LOLMatchTrackerApp('ritomatchs.db')
    app.run()
