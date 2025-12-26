import os 
from dotenv import load_dotenv
from urllib.parse import quote
import requests
import json

load_dotenv()
Rito_api =  os.getenv("RitoDevAPI")
if Rito_api is None:
    print("error loading")

#Account detail 
gameName = input("Summoners name : ")
gameTag = input("#tag : ")
print(gameName+"#"+gameName)
parseGamename = quote(gameName)

#Get Account name and tag line 
getAccountinfoi = (f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{parseGamename}/{gameTag}?api_key={Rito_api}")
getPUIDfromAccount = requests.get(getAccountinfoi)
cacheUserInfo = []
cacheUserInfo = getPUIDfromAccount.json()
session_userPUUID =cacheUserInfo["puuid"]
# print(session_userPUUID)

#matchaHistory 
getMatchid = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{session_userPUUID}/ids?start=0&count=20&api_key={Rito_api}"

gameType = {
    "solo":"420",
    "draft":"400",
    "flex":"440"
    }

while True:
    modePicker = input("please type draft, solo or flex for game mode you want to look into : ").lower().strip()
    if modePicker in gameType:
        chosenQueue_id = gameType[modePicker]
        print(f"Checking chosen {modePicker} type")
        break
    else:
        print("Type not listed, try again")

# below no longer needed but can uncomment for testing  as PUUID dont change
# session_userPUUID = "ZYWPgJTPG4vG_LhHnqmPqKVUY49kBJxZ5xEF8v32ZL0XQwNlpVY4_bQpY6UTeBUtgCTR-yl5xwwO1Q"
getRankMatchid = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{session_userPUUID}/ids?start=&queue={chosenQueue_id}&count=20&api_key={Rito_api}"
gamesIDs = requests.get(getRankMatchid)

gamesIDHistory = []
gamesIDHistory = gamesIDs.json()
# print(gamesIDs.json())

# Queue ID	Mode    Name
# 400	Normal  Draft	Good for testing "Serious but not Ranked" play.
# 420 	Ranked  Solo	Your main target for performance stats.
# 440	Ranked  Flex	Good for "Team-based" analysis.



#Match information 
gameID_array = gamesIDHistory[1]
getMatchinfo = f"https://europe.api.riotgames.com/lol/match/v5/matches/{gameID_array}?api_key={Rito_api}"
gameData = requests.get(getMatchinfo)
print(gameData.json())
