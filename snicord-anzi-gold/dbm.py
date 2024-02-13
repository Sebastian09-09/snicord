import json 

def getConfig():
    with open("config.json", "r") as f:
        return json.load(f)

def setConfig(data):
    with open("config.json","w") as f:
        json.dump(data,f)  

def getTiming():
    with open("timing.json", "r") as f:
        return json.load(f)

def setTiming(data):
    with open("timing.json","w") as f:
        json.dump(data,f)  

def getAlerts():
    with open("rarityAlerts.json", "r") as f:
        return json.load(f)

def setAlerts(data):
    with open("rarityAlerts.json","w") as f:
        json.dump(data,f)  

def getChannels(bot):
    with open(f"{bot}channels.json", "r") as f:
        return json.load(f)

def setChannels(bot,data):
    with open(f"{bot}channels.json", "w") as f:
        json.dump(data,f)