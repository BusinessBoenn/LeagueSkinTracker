import os
import psutil
import json
from collections import defaultdict
from lcu_driver import Connector
import sys

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

connector = Connector()


def cleanData(connection, skindata):

    #strip skin data of unnecessary data
    cleanData = []
    for item in skindata:
        cleanData.append({"championId": item["championId"], "id": item["id"], "name": item["name"], "owned": item["ownership"]["owned"], "tilePath": item["tilePath"], "isBase": item["isBase"]})
    
    #group skins by championId
    grouped = defaultdict(list)
    for d in cleanData:
        key_value = d.get("championId")
        grouped[key_value].append(d)
    group = dict(grouped)

    #rename datasets like champion instead of championId
    keys = []
    names = []

    for x, y in group.items():
        names.append(y[0]["name"])
        keys.append(x)

    for i in range(0, len(names)):

        #exclude Doom Bot entries
        if "Doom Bot" in group[keys[i]][0]["name"]:
            group.pop(keys[i])
        else:
            group[names[i]] = group.pop(keys[i])


    #count and track if skins are owned or not
    skins ={}

    for x, y in group.items():
        total = 0
        owned = 0
        skins[x] = {}

        for i in range (0, len(y)):
            if y[i]["isBase"]:
                continue
            total += 1
            if y[i]["owned"]:
                owned += 1

            skins[x][y[i]["name"]] = y[i]["owned"]

        skins[x]["total"] = total
        skins[x]["owned"] = owned
        skins[x]["id"] = y[0]["championId"]


        with open("finaln.json", "w") as f:
            json.dump(dict(sorted(skins.items())), f, indent=2)


    
    



@connector.ready
def connect(connection):


    summoner = connection.request("get", "/lol-summoner/v1/current-summoner/account-and-summoner-ids")

    if summoner.status != 200:
        print("Something went wrong while sending the first request")
        sys.exit()

    sum = summoner.json()
    summonerId = str(sum["summonerId"])

    skins = connection.request("get", "/lol-champions/v1/inventories/"+summonerId+"/skins-minimal").json()
    loot = connection.request("get", "/lol-loot/v1/player-loot").json()
    cleanData(connection, skins)


@connector.close
async def disconnect(connection):
    print("Connector closed")



connector.start()