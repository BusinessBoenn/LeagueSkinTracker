import os
from lcu_driver import Connector
import json


path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)


connector = Connector()



@connector.ready
async def connect(connection):
    try:

        summonerdata = await connection.request("get", "/lol-summoner/v1/current-summoner/account-and-summoner-ids")

        sum = await summonerdata.json()
        summonerId = sum["summonerId"]


        sessiondata = await connection.request("get", "/lol-champ-select/v1/session")
        session =  await sessiondata.json()
        with open("final.json", "r") as f:
            champs = json.load(f)


        picked_champs = []
        picked_champs_name = []

        for x in session["myTeam"]:
            if x["summonerId"] == summonerId:
                my_champ = x["championId"]
                my_champ_name = champs[str(x["championId"])]["name"]
            else:
                picked_champs.append(x["championId"])
                picked_champs_name.append(champs[str(x["championId"])]["name"])


        available_champs =[]
        available_champs_name =[]

        for x in session["benchChampions"]:
            available_champs.append(x["championId"])
            available_champs_name.append(champs[str(x["championId"])]["name"])

        
        print("My champ: ", my_champ)
        print("My champ name: ", my_champ_name)
        print("Picked champs: ", picked_champs)
        print("Picked champs names: ", picked_champs_name)
        print("Available champs: ", available_champs)
        print("Available champs names: ", available_champs_name)
        
    except Exception as e:
        print(f"An error occurred: {e}")




@connector.close
async def disconnect(connection):
    print("Task done!")


connector.start()