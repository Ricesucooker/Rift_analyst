import time
import json
import api_client
from database import setup_db, add_match
from urllib.parse import quote


class MatchEngine:
    """
    MatchEngine
    core logic for the application. 

    """
    def __init__(self, database ):
        self.puuid = None
        self.database = database
        setup_db(self.database)
        
    def setup_user(self, name:str, tag:str):
        """
        setup_user
        
        Get infomration 

        Get the puuid of the user 
        
        :param name: username
        :type name: str
        :param tag: user tag
        :type tag: str
        """
        self.game_name:str = name
        self.game_tag:str = tag 
        self.puuid = api_client.getPUIDinfo(quote(name),tag)
        if self.puuid != "Account not found" :
            return True
        else:   
            return False
    
    def set_gamemode(self, gamemode:str ):
        """
        set_gamemode

        Selection of the game mode solo, draft or flex 
        
        :param self: 
        :param gamemode: game mode type 
        :type gamemode: 
        """
        gameType = {
        "solo":"420",
        "draft":"400",
        "flex":"440"
        }
        self.chose_queue_id = None
        if gamemode in gameType:
            self.chose_queue_id = gameType[gamemode]
            print(f"checking game mode:{gamemode}")
            return True
        else:
            print(f"Mode not valid!")
            return False 
        
    def get_match_list(self):
        self.gameHistory = [] 
        api_call = api_client.getQueue_matchID(self.puuid, self.chose_queue_id)
        if api_call != "No match history found":
            self.gameHistory = api_call
        else:
            self.gameHistory = []

    def get_matchdata(self):
        """
        get_matchdata
        logic to get last 10 matcha data 
        
        :param self: Description

        """
        self.raw_data = []
        for matchID in self.gameHistory[:20]:
            data = api_client.getGameinfo_fromMatch(matchID)
            if isinstance(data, dict):
                self.raw_data.append(data)
                time.sleep(1.5)

        for gameParticipated in self.raw_data:
            participantList = gameParticipated["info"]["participants"]
            for player in participantList:
                if player["puuid"] == self.puuid:
                    match_id = gameParticipated["metadata"]["matchId"]
                    match_blob = json.dumps(gameParticipated)
                    add_match(
                        self.database,
                        match_id,
                        self.game_name,
                        player['championName'],
                        player['kills'],
                        player['deaths'],
                        player['assists'],
                        player['win'],
                        player['totalDamageDealt'],
                        match_blob)
                    print(f" debug: MatchID type: {type({match_id})}, match blob tye:{type(match_blob)}" )
                    print(f"User : {self.game_name},\nChampion : {player['championName']}")
                    if player["win"] is True:
                        print(f"Game Won with KDA:{player['kills']}/{player['deaths']}/{player['assists']} \nTotal Damage: {player['totalDamageDealt']} \nDamage to Champions:{player['totalDamageDealtToChampions']}")
                    else:
                        print(f"Game Loss with KDA:{player['kills']}/{player['deaths']}/{player['assists']} \nTotal Damage: {player['totalDamageDealt']} \nDamaage to Champions:{player['totalDamageDealtToChampions']}")
                    break



        