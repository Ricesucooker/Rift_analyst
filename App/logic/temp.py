import os
from dotenv import load_dotenv
import requests

load_dotenv()
Rito_api =  os.getenv("RitoDevAPI")

uri = f'https://europe.api.riotgames.com/lol/match/v5/matches/EUW1_7657028499?api_key={Rito_api}'
data = requests.get(uri)

matchJSON = data.json()

print(type(matchJSON["info"]["participants"]))

print(matchJSON["info"]["participants"][0]["puuid"])

for player in matchJSON["info"]["participants"]:

    if player["puuid"] == "ZYWPgJTPG4vG_LhHnqmPqKVUY49kBJxZ5xEF8v32ZL0XQwNlpVY4_bQpY6UTeBUtgCTR-yl5xwwO1Q":
        print(f" {player['riotIdGameName']} : {player['championName']}: {player['lane']} ")
        print(f"KDA: {player['kills']}/{player['deaths']}/{player['assists']}")
        if player["win"] is True:
            print ("Game won")
        else:
            print("Game loss")
        break