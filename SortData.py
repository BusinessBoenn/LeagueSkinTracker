import os
import json
from collections import defaultdict

path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

def GroupData(data):
    grouped = defaultdict(list)
    for d in data:
        key_value = d.get("championId")
        grouped[key_value].append(d)
    return dict(grouped)

    
    

if __name__ == "__main__":
    with open("cleanedData.json", "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    

    groupedData = GroupData(data)

    with open("groupedData.json", "w", encoding="utf-8-sig") as f:
        json.dump(groupedData, f, indent=2)