import os
import time
from dotenv import load_dotenv
from urllib.parse import quote
import requests

load_dotenv()
Rito_api =  os.getenv("RitoDevAPI")
if Rito_api is None:
    print("error loading")

def userAccount(gameName:str, gameTag:str):
    return f"{gameName}#{gameTag}"


#Getting PUID
def getPUIDinfo(parseGamename:str, gameTag:str):
    """
    getPUIDinfo 
    API request to get the puuid 
    
    :param parseGamename: required 
    :type parseGamename: str
    :param gameTag: required
    :type gameTag: str
    """
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
    """
    getQueue_matchID
    API request that get to get the last 20 games from chosen game type 
    
    :param cachedPUUID:  required player puuid from getPUIDinfo
    :type cachedPUUID: str
    :param chosenQueue_id: Queue type i.e solo, rank, flex ect..  
    :type chosenQueue_id: str
    """
    getGames_fromQueue =f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{cachedPUUID}/ids?start=0&queue={chosenQueue_id}&count=20&api_key={Rito_api}"
    gamesIDs = requests.get(getGames_fromQueue)
    if gamesIDs.status_code ==200:
        return gamesIDs.json()
    else:
        return "No match history found"

#getting match information
def getGameinfo_fromMatch(gameID_list:str):
    """
    getGameinfo_fromMatch

    API request using the gameID to pull the data from rito api using matchID
    
    :param gameID_list: Description
    :type gameID_list: str
    """
    getGameinfo = f"https://europe.api.riotgames.com/lol/match/v5/matches/{gameID_list}?api_key={Rito_api}"
    gameData = requests.get(getGameinfo)
    if gameData.status_code ==200:
        return gameData.json() 
    else:
        return "No game information found"

