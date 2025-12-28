import os
import time
from dotenv import load_dotenv
from urllib.parse import quote
import requests

load_dotenv()
Rito_api =  os.getenv("RitoDevAPI")
if Rito_api is None:
    print("error loading")

#Account detail 
gameName = input("Summoners name : ")
gameTag = input("# Tag : ")
parseGamename = quote(gameName)

def userAccount(gameName:str, gameTag:str):
    return f"{gameName}#{gameTag}"

print(f"Checking account : {userAccount(gameName,gameTag)}")

#Getting PUID
def getPUIDinfo(parseGamename:str, gameTag:str):
    getAccountinfo =(f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{parseGamename}/{gameTag}?api_key={Rito_api}")
    getPUUID_fromAccount = requests.get(getAccountinfo)
    if getPUUID_fromAccount.status_code ==200:
        cachedUserInfo  = getPUUID_fromAccount.json()
        session_userPUUID = cachedUserInfo["puuid"]
        print("Account found getting information...")
        return f"{session_userPUUID}"
    else:
        return "Account not found"

#getting match list 
def getQueue_matchID(cachedPUUID:str,chosenQueue_id:str):
    getGames_fromQueue =f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{cachedPUUID}/ids?start=0&queue={chosenQueue_id}&count=20&api_key={Rito_api}"
    gamesIDs = requests.get(getGames_fromQueue)
    if gamesIDs.status_code ==200:
        return gamesIDs.json()
    else:
        return "No match history found"

#getting match information
def getGameinfo_fromMatch(gameID_list:str):
    getGameinfo = f"https://europe.api.riotgames.com/lol/match/v5/matches/{gameID_list}?api_key={Rito_api}"
    gameData = requests.get(getGameinfo)
    if gameData.status_code ==200:
        return gameData.json() 
    else:
        return "No game information found"


#if all above work should retrun:
# !username#gamertag and puuid     
cachedPUUID = getPUIDinfo(parseGamename,gameTag)

if cachedPUUID !='Account not found':

    gameType = {
        "solo":"420",
        "draft":"400",
        "flex":"440"
        }

    while True:
        modePicker = input("Please type draft, solo or flex for game mode you want to look into : ").lower().strip()
        if modePicker in gameType:
            chosenQueue_id = gameType[modePicker]
            print(f"Checking chosen {modePicker} type")
            break
        else:
            print("Type not listed, try again")
    
    gameHistory = getQueue_matchID(cachedPUUID, chosenQueue_id)
    gameID_list = gameHistory

    # print(getGameinfo_fromMatch(gameID_list))
    
    rawMatch_data = []

    for matchID in gameHistory[:10]:
        data = getGameinfo_fromMatch(matchID)
        if  isinstance(data, dict):
            rawMatch_data.append(data)
            print(f"Found match ID: {matchID} saved")
            time.sleep(1.5)
        else:
            print(f"Error finding game info from match id {matchID} : {data}")
            time.sleep(1.2)

    for gameParticipated in rawMatch_data:
        participantList = gameParticipated["info"]["participants"]

        for player in participantList:
            if player["puuid"] == cachedPUUID:
                print(f"User : {gameName},\nChampion : {player['championName']}")
                if player["win"] is True:
                    print(f"Game Won with KDA:{player['kills']}/{player['deaths']}/{player['assists']} \nTotal Damage: {player['totalDamageDealt']} \nDamage to Champions:{player['totalDamageDealtToChampions']}")
                else:
                    print(f"Game Loss with KDA:{player['kills']}/{player['deaths']}/{player['assists']} \nTotal Damage: {player['totalDamageDealt']} \nDamaage to Champions:{player['totalDamageDealtToChampions']}")
                break

else:
    print("Stoppping script because user was not found.")


