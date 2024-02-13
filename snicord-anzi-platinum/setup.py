import os

print("Snicord (anzi) Platinum")
tokens = []
configData = {
    "prefix": ">",
    "controllerAccountID": "",
    "anigameSniper": "on",
    "anigamePrefix": ".",
    "izziSniper": "on",
    "izziPrefix": "iz ",
    "latency": "off",
    "latency_": 0,
    "alerts": "on",
    "alertsChannel": "",
    "anigameLottery": "off",
    "anigameHourly": "off",
    "anigameBtAll": "off",
    "anigameRdBtAll": "off",
    "anigameLocClearer": "off",
    "izziLottery": "off",
    "izziHourly": "off",
    "izziBtAll": "off",
    "izziRdBtAll": "off",
    "izziEvBtAll": "off",
    "izziLocClearer": "off",
    "featuresChannel": "",
    "commandsChannel": ""
}

for i in configData:
    a = input(f"{i} : ")
    configData[i] = a

tokensLen = int(input("how many tokens will you like to use : "))
with open("secret.txt", "w") as t:
    for i in range(1, tokensLen + 1):
        token = input(f"token {i} : ")
        tokens.append(token)
        t.write(f'DISCORD_TOKEN{i}="{token}"\n')
        db = token.split(".")[1]
        if db not in os.listdir("accounts"):
            os.mkdir(f"accounts/{db}", 0o006)
        with open(f"accounts/{db}/anigamechannels.json", "w") as f:
            f.write("{}")
        with open(f"accounts/{db}/izzichannels.json", "w") as f:
            f.write("{}")
        with open(f"accounts/{db}/rarityAlerts.json", "w") as f:
            f.write(
                '{"anigame": ["super rare", "ultra rare"], "izzi": ["diamond"]}'
            )
        with open(f"accounts/{db}/timing.json", "w") as f:
            f.write(
                '{"anigameHourly": 3600, "anigameLottery": 610, "anigameBtAll": 1810, "anigameRdBtAll":1810, "anigameLocClearer":3610, "izziHourly": 3610, "izziLottery": 910, "izziBtAll": 1810, "izziRdBtAll":1810, "izziEvBtAll":1810, "izziLocClearer":3610 ,"spamDelay": 5}'
            )
        with open(f"accounts/{db}/config.json", "w") as f:
            configData["prefix"] += str(i)
            f.write(str(configData).replace("'", '"'))
            configData["prefix"] = configData["prefix"].rstrip(str(i))
        with open(f"accounts/{db}/keepSpamming.json", "w") as f:
            f.write("{}")
        with open(f"accounts/{db}/location.json", "w") as f:
            f.write('{"anigame":["1","1"],"izzi":["1","1"]}')