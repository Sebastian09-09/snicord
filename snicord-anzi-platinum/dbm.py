import json 

def getConfig(db):
    with open(f"accounts/{db}/config.json", "r") as f:
        return json.load(f)

def setConfig(db,data):
    with open(f"accounts/{db}/config.json","w") as f:
        json.dump(data,f)  

def getTiming(db):
    with open(f"accounts/{db}/timing.json", "r") as f:
        return json.load(f)

def setTiming(db,data):
    with open(f"accounts/{db}/timing.json","w") as f:
        json.dump(data,f)  

def getAlerts(db):
    with open(f"accounts/{db}/rarityAlerts.json", "r") as f:
        return json.load(f)

def setAlerts(db,data):
    with open(f"accounts/{db}/rarityAlerts.json","w") as f:
        json.dump(data,f)  

def getChannels(db,bot):
    with open(f"accounts/{db}/{bot}channels.json", "r") as f:
        return json.load(f)

def setChannels(db,bot,data):
    with open(f"accounts/{db}/{bot}channels.json", "w") as f:
        json.dump(data,f)

def getSpam(db):
    with open(f"accounts/{db}/keepSpamming.json","r") as f:
        return json.load(f) 

def setSpam(db,data):
    with open(f"accounts/{db}/keepSpamming.json","w") as f:
        json.dump(data,f) 

def getLoc(db):
    with open(f"accounts/{db}/location.json","r") as f:
        return json.load(f)

def setLoc(db,data):
    with open(f"accounts/{db}/location.json","w") as f:
        json.dump(data,f) 
