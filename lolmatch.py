import sys, os, requests, json, datetime

API_AMERICAS = "https://americas.api.riotgames.com/lol/match/v5/matches/"
API_ASIA = "https://asia.api.riotgames.com/lol/match/v5/matches/"
API_EUROPE = "https://europe.api.riotgames.com/lol/match/v5/matches/"
API_SEA = "https://sea.api.riotgames.com/lol/match/v5/matches/"

class player:
    def __init__(self, name, level, role, champ):
        self.name = name
        self.level = level
        self.role = role
        self.champ = champ

if os.path.isfile("key.txt"):
    KEY = open("key.txt").readline()
else:
    print("No key.txt file with key")
    exit()

AMERICAS_PRE = ["NA1", "BR1", "LA1", "LA2"] #4
ASIA_PRE = ["KR", "JP1"] #2
EUROPE_PRE = ["EUN1", "EUW1", "TR1", "RU"] #4
SEA_PRE = ["OC1", "PH2", "SG2", "TH2", "TW2", "VN2"] #6 = 16

def matchreq(url, gameID):
    # print(url + gameID + "?api-key=" + KEY)
    response = requests.get(url + gameID + "?api_key=" + KEY)
    if response.ok:
        return response
    else:
        return "400"

def main(arg):
    region = "null"

    if arg == "none":
        gameID = input("Game ID: ")
    else:
        gameID = arg
    
    
    if "_" in gameID:
        region = gameID.split("_")[0].upper()
        gameID = gameID.split("_")[1]
    
    if region == "null":
        # check all regions for match
        id = "_"+gameID
        for pre in AMERICAS_PRE:
            print("checking " + pre+id + "...")
            response = matchreq(API_AMERICAS, pre+id)
            if response != "400":
                return response.json()
            
        for pre in EUROPE_PRE:
            print("checking " + pre+id + "...")
            response = matchreq(API_EUROPE, pre+id)
            if response != "400":
                return response.json()
            
        for pre in SEA_PRE:
            print("checking " + pre+id + "...")
            response = matchreq(API_SEA, pre+id)
            if response != "400":
                return response.json()
            
        for pre in ASIA_PRE:
            print("checking " + pre+id + "...")
            response = matchreq(API_ASIA, pre+id)
            if response != "400":
                return response.json()

    else:
        # check selected region
        if region in AMERICAS_PRE:
            print("checking " + region+"_"+gameID + "...")
            response = matchreq(API_AMERICAS, region + "_" + gameID)
            if response != "400":
                return response.json()
        
        if region in EUROPE_PRE:
            print("checking " + region+"_"+gameID + "...")
            response = matchreq(API_EUROPE, region + "_" + gameID)
            if response != "400":
                return response.json()

        if region in SEA_PRE:
            print("checking " + region+"_"+gameID + "...")
            response = matchreq(API_SEA, region + "_" + gameID)
            if response != "400":
                return response.json()
        
        if region in ASIA_PRE:
            print("checking " + region+"_"+gameID + "...")
            response = matchreq(API_ASIA, region + "_" + gameID)
            if response != "400":
                return response.json()

    return "No Results for GameId: " + gameID

if len(sys.argv) > 1:
    jsonobj = main(sys.argv[1])
else:
    jsonobj = main("none")

def createfile(fname):
    if os.path.isfile(fname):
        os.remove(fname)
    return open(fname, "x")

if type(jsonobj) is not str:
    print("Found game, creating json and parsed text file")

    # create json
    fnamejson = jsonobj["metadata"]["matchId"]+".json"
    # if os.path.isfile(fname): # delete if already exists for some reason
    #     os.remove(fname)
    # file = open(fname, "x")
    jsonfile = createfile(fnamejson)
    jsonfile.write(json.dumps(jsonobj, indent=4))

    # create text for file
    info = jsonobj["info"]
    time = datetime.datetime.fromtimestamp(info["gameCreation"]/1000).strftime('%Y-%m-%d %H:%M:%S')
    version = info["gameVersion"]
    blueSide = list()
    redSide = list()
    for obj in info["participants"]:
        newplayer = player(name= obj["summonerName"], level= obj["summonerLevel"], role= obj["teamPosition"], champ= obj["championName"])
        if obj["teamId"] == 100: # blue side
            blueSide.append(newplayer)
        else:
            redSide.append(newplayer)

    textff = f'MatchID: {jsonobj["metadata"]["matchId"]}\nDate: {time}\nVersion: {version}'

    textff += "\n\nBlueSide\n----------"
    for player in blueSide:
        textff+=f"\n- {player.name}, Lvl {player.level}\nPlaying {player.champ} in {player.role}"

    textff+="\n\nRedSide\n----------"
    for player in redSide:
        textff+=f"\n- {player.name}, Lvl {player.level}\nPlaying {player.champ} in {player.role}"

    # create file
    fnametxt = jsonobj["metadata"]["matchId"]+".txt"
    filetxt = createfile(fnametxt)
    filetxt.write(textff)
else:
    print(jsonobj)