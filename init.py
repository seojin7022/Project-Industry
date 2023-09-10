import os, json, datetime
from settings import *

if not os.path.exists(f"./data"):
    os.mkdir("./data")


def InspectData(data: dict, playerData: dict):
    for v in data.keys():
        if playerData.get(v):
            if type(data[v]) == dict:
                playerData[v] = InspectData(data[v], playerData[v])
        else:
            print(v)
            playerData[v] = data[v]

    return playerData


datas = {

    "Money": 0,
    "Map": [["0" for i in range(MAP_SIZE[0])] for j in range(MAP_SIZE[1])],
    "MachineMap": [["0" for i in range(MAP_SIZE[0])] for j in range(MAP_SIZE[1])],
    "Machines": {
        "Peel_Machine": 0,
    },
    "Inventory": {
        "Oak_0": 0,
        "Oak_1": 0,
        "Oak_2": 0,
        "Oak_3": 0,
    },

    "Clock": [2023, 1, 1, 0, 0]
}

data = {}
isFirstStarter = True

if os.path.exists(f"./data/player-data.txt"):
    isFirstStarter = False
    with open(f"./data/player-data.txt", "r") as playerData:
        data = InspectData(datas, json.loads(playerData.read()))
else:
    with open(f"./data/player-data.txt", "w") as playerData:
        playerData.write(json.dumps(datas))
        data = datas

print("✅ Initialized Successfully")
