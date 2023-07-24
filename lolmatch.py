import requests, os, json

API_AMERICAS = "https://americas.api.riotgames.com/lol/match/v5/matches/"
API_ASIA = "https://asia.api.riotgames.com/lol/match/v5/matches/"
API_EUROPE = "https://europe.api.riotgames.com/lol/match/v5/matches/"
API_SEA = "https://sea.api.riotgames.com/lol/match/v5/matches/"

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

def main():
    region = "null"
    gameID = input("Game ID: ")
    
    
    if "_" in gameID:
        region = gameID.split("_")[0]
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
            response = matchreq(API_AMERICAS, region + "_" + gameID)
            if response != "400":
                return response.json()
        
        if region in EUROPE_PRE:
            response = matchreq(API_EUROPE, region + "_" + gameID)
            if response != "400":
                return response.json()

        if region in SEA_PRE:
            response = matchreq(API_SEA, region + "_" + gameID)
            if response != "400":
                return response.json()
        
        if region in ASIA_PRE:
            response = matchreq(API_ASIA, region + "_" + gameID)
            if response != "400":
                return response.json()

    return "No Results for " + gameID

jsonobj = main()

if jsonobj is not str:
    fname = jsonobj["metadata"]["matchId"]+".json"
    if os.path.isfile(fname):
        os.remove(fname)
    file = open(fname, "x")
    file.write(json.dumps(jsonobj, indent=4))
