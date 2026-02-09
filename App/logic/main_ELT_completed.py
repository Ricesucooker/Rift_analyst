from duckdb_analytics import MatchAnalyst
from engine import MatchEngine

ro_database = 'ritomatchs.db'


scriptLogic = MatchEngine(ro_database)

gameName = input("Summoners name : ")
gameTag = input("# Tag : ")

scriptLogic.setup_user(gameName,gameTag)

while True:
    modePicker = input("Please type [draft], [solo] or [flex] for the game mode data you are looking to pull:\n") .lower().strip()
    if scriptLogic.set_gamemode(modePicker) != False:
        break

scriptLogic.get_match_list()
scriptLogic.get_matchdata()


gameTracker = MatchAnalyst(ro_database)
gameTracker.view_recent_games()
gameTracker.get_best_champion_KDA()
