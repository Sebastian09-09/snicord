import json 

def getConfig():
    with open(r"config.json", "r") as f:
        return json.load(f)

def getChannels():
    with open(r"channels.json", "r") as f:
        return json.load(f)