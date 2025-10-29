import os
import json

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

def CleanData():

    cleanData = []
    with open("skins.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    for item in data:
        cleanData.append({"championId": item["championId"], "id": item["id"], "name": item["name"], "owned": item["ownership"]["owned"], "tilePath": item["tilePath"], "isBase": item["isBase"]})
    
    with open("cleanedData.json", "w", encoding="utf-16") as f:
        json.dump(cleanData, f, indent=2)
    
if __name__ == "__main__":
    CleanData()