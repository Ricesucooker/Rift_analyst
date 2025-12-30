import database
import sqlite3


dbName='ritomatchs.db'

def viewMatch():
    with sqlite3.connect(dbName) as connection:
        cursor = connection.cursor()
        
        viewMatch_query=''' Select 
        match_id,
        summoner_name,
        kills,
        deaths,
        assists
        from match_stats'''
    
        cursor.execute(viewMatch_query)
        all_matches = cursor.fetchall()

    for row in all_matches:
        print(f"Match: {row[0]} | Player: {row[1]} | Kills: {row[2]} | Death: {row[3]} | Assist{row[4]}")


def viewGameAvgKDA():
    with sqlite3.connect(dbName) as connection:
        cursor = connection.cursor()

        viewAllMatchesKDA_query='''Select 
        match_id,
        summoner_name,
        Case 
        When Deaths > 0 Then
        (Kills+Assists)/cast(Deaths as float)
        Else   
        (Kills+Assists)/(Deaths +1) end as AvgKDA
        from match_stats'''

        cursor.execute(viewAllMatchesKDA_query)
        kda_Allmatch = cursor.fetchall()

    for row in kda_Allmatch:
        print(f"Match: {row[0]} | Summoner: {row[1]} | AvgKDA: {round(row[2],2)}")


#callfunction 

viewMatch()

viewGameAvgKDA()