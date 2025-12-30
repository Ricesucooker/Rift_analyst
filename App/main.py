import time
from urllib.parse import quote
import json
import api_client
from database import setup_db, add_match

setup_db()

#Account detail 
gameName = input("Summoners name : ")
gameTag = input("# Tag : ")
parseGamename = quote(gameName)

def userAccount(gameName:str, gameTag:str):
    return f"{gameName}#{gameTag}"

print(f"Checking account : {userAccount(gameName,gameTag)}")


#if all above work should retrun:
# !username#gamertag and puuid     
cachedPUUID = api_client.getPUIDinfo(parseGamename,gameTag)

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
    
    gameHistory = api_client.getQueue_matchID(cachedPUUID, chosenQueue_id)
    gameID_list = gameHistory

    # print(getGameinfo_fromMatch(gameID_list))
    
    rawMatch_data = []

    for matchID in gameHistory[:10]:
        data = api_client.getGameinfo_fromMatch(matchID)
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
                match_id = gameParticipated["metadata"]["matchId"]
                match_blob = json.dumps(gameParticipated)
                add_match(
                    match_id,
                    gameName,
                    player['championName'],
                    player['kills'],
                    player['deaths'],
                    player['assists'],
                    player['win'],
                    player['totalDamageDealt'],
                    match_blob)
                print(f" debug: MatchID type: {type({match_id})}, match blob tye:{type(match_blob)}" )
                print(f"User : {gameName},\nChampion : {player['championName']}")
                if player["win"] is True:
                    print(f"Game Won with KDA:{player['kills']}/{player['deaths']}/{player['assists']} \nTotal Damage: {player['totalDamageDealt']} \nDamage to Champions:{player['totalDamageDealtToChampions']}")
                else:
                    print(f"Game Loss with KDA:{player['kills']}/{player['deaths']}/{player['assists']} \nTotal Damage: {player['totalDamageDealt']} \nDamaage to Champions:{player['totalDamageDealtToChampions']}")
                break

else:
    print("Stoppping script because user was not found.")



