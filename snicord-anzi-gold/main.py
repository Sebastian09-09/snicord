import discum
import dbm  
import requests
import time 
import threading 
import os 
from dotenv import load_dotenv
load_dotenv()
from rich.console import Console
console = Console()


from os import system, name
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

#Styles 
defaultStyle = "bold #FFFFFF"
specialStyle = "bold #5D88BB"
snipeStyle = "bold #A1A8B2"
infoStyle = "bold #B3CBE4"
warningStyle = "bold #fc9d03"
errorStyle = "bold #fc3903"

class Selfbot:
    def __init__(self,token):
        self.token = token
        #ConfigData 
        self.configData = dbm.getConfig()
        self.prefix = self.configData["prefix"]
        self.alerts = self.configData["alerts"]
        self.latency = self.configData["latency"]
        self.latency_ = int(self.configData["latency_"])
        self.anigameHourly = self.configData["anigameHourly"]
        self.anigameLottery = self.configData["anigameLottery"]
        self.izziHourly = self.configData["izziHourly"]
        self.izziLottery = self.configData["izziLottery"]
        self.anigamePrefix = self.configData["anigamePrefix"]
        self.izziPrefix = self.configData["izziPrefix"]
        #SelfBot Channels 
        self.alertsChannel = self.configData["alertsChannel"]
        self.featuresChannel = self.configData["featuresChannel"]
        self.commandsChannel = self.configData["commandsChannel"]
        #Sniper 
        self.anigameSniper = self.configData["anigameSniper"]
        self.izziSniper = self.configData["izziSniper"]
        #Sniping Channels 
        self.anigameChannels = dbm.getChannels("anigame")
        self.izziChannels = dbm.getChannels("izzi")
        #User
        self.user = self.getUserData(self.alertsChannel)
        console.print(f'User     - {self.user["username"]}#{self.user["discriminator"]}\nPrefix   - {self.prefix}', style=defaultStyle, justify="left")
    
    def hourlyAnigame(self):
        while self.anigameHourly == "on":
            self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}hourly")
            time.sleep(3610)

    def lotteryAnigame(self):
        while self.anigameLottery == "on":
            time.sleep(2) #Static Pause for 1 second
            self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}lottery")
            time.sleep(610)

    def hourlyIzzi(self):
        while self.izziHourly == "on":
            self.sendMessage(self.featuresChannel, f"{self.izziPrefix}hourly")
            time.sleep(3610)

    def lotteryIzzi(self):
        while self.izziLottery == "on":
            time.sleep(2) #Static Pause for 1 second 
            self.sendMessage(self.featuresChannel, f"{self.izziPrefix}lottery")
            time.sleep(910) 

    def startThread(self,func):
        thr = threading.Thread(target=func, daemon=True) 
        thr.start() 
        return thr 
        
    def run(self):
        self.bot = discum.Client(token=self.token, log=False)

        if self.anigameHourly == "on":
            self.hourlyAnigameThread = self.startThread(self.hourlyAnigame)

        if self.anigameLottery == "on":
            self.lotteryAnigameThread = self.startThread(self.lotteryAnigame)
            
        if self.izziHourly == "on":
            self.hourlyIzziThread = self.startThread(self.hourlyIzzi)

        if self.izziLottery == "on":
            self.lotteryIzziThread = self.startThread(self.lotteryIzzi)

        @self.bot.gateway.command
        def selfbot(resp):
            if resp.event.message:
                m = resp.parsed.auto() 
                #Commands 
                if m["author"]["id"] == self.user["id"] and m['channel_id'] == self.commandsChannel:
                    #Toggle Latency 
                    if m["content"] == f"{self.prefix}toggle latency":
                        if self.latency == "on":
                            self.latency = "off"
                            self.configData["latency"] = "off"
                            console.print(f'👍 latency - 🟥 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 latency - 🟥 `")
                        else:
                            self.latency = "on"
                            self.configData["latency"] = "on"
                            console.print(f'👍 latency - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 latency - 🟩 `")

                        dbm.setConfig(self.configData) 

                    #Toggle Alerts 
                    elif m["content"] == f"{self.prefix}toggle alerts":
                        if self.alerts == "on":
                            self.alerts = "off"
                            self.configData["alerts"] = "off"
                            console.print(f'👍 alerts - 🟥 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 alerts - 🟥 `")
                        else:
                            self.alerts = "on"
                            self.configData["alerts"] = "on"
                            console.print(f'👍 alerts - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 alerts - 🟩 `")

                        dbm.setConfig(self.configData) 

                    #Toggle Anigame Sniper 
                    elif m["content"] == f"{self.prefix}toggle anigame sniper":
                        if self.anigameSniper == "on":
                            self.anigameSniper = "off"
                            self.configData["anigameSniper"] = "off"
                            console.print(f'👍 anigame sniper - 🟥 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame sniper - 🟥 `")
                        else:
                            self.anigameSniper = "on"
                            self.configData["anigameSniper"] = "on"
                            console.print(f'👍 anigame sniper - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame sniper - 🟩 `")

                        dbm.setConfig(self.configData) 

                    #Toggle Anigame Hourly 
                    elif m["content"] == f"{self.prefix}toggle anigame hourly":
                        if self.anigameHourly == "on":
                            self.anigameHourly = "off"
                            self.configData["anigameHourly"] = "off"
                            console.print(f'👍 anigame hourly - 🟥 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame hourly - 🟥 `")
                        else:
                            self.anigameHourly = "on"
                            self.configData["anigameHourly"] = "on"
                            try:
                                if not self.hourlyAnigameThread.is_alive():
                                    self.hourlyAnigameThread = self.startThread(self.hourlyAnigame) 
                            except AttributeError:
                                self.hourlyAnigameThread = self.startThread(self.hourlyAnigame)
                            console.print(f'👍 anigame hourly - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame hourly - 🟩 `")

                        dbm.setConfig(self.configData) 

                    #Toggle Anigame Lottery 
                    elif m["content"] == f"{self.prefix}toggle anigame lottery":
                        if self.anigameLottery == "on":
                            self.anigameLottery = "off"
                            self.configData["anigameLottery"] = "off"
                            console.print(f'👍 anigame lottery - 🟥 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame lottery - 🟥 `")
                        else:
                            self.anigameLottery = "on"
                            self.configData["anigameLottery"] = "on"
                            try:
                                if not self.lotteryAnigameThread.is_alive():
                                    self.lotteryAnigameThread = self.startThread(self.lotteryAnigame)
                            except AttributeError:
                                self.lotteryAnigameThread = self.startThread(self.lotteryAnigame)
                            console.print(f'👍 anigame lottery - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame lottery - 🟩 `")

                        dbm.setConfig(self.configData) 

                    #Add Anigame Sniper Channel 
                    elif m["content"].startswith(f"{self.prefix}add chan anigame "):
                        cont = m["content"].split(" ")
                        name = cont[-1]
                        id_ = cont[-2]
                        if id_ not in self.anigameChannels:
                            self.anigameChannels[id_] = name
                            console.print(f'👍 anigame >> {name} - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 anigame >> {name} - 🟩 `")
                            dbm.setChannels("anigame",self.anigameChannels)
                        else:
                            console.print(f'🤨 anigame >> {name} is already being sniped! ', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 anigame >> {name} is already being sniped! `")

                    #Remove Anigame Sniper Channel 
                    elif m["content"].startswith(f"{self.prefix}rem chan anigame "):
                        cont = m["content"].split(" ")
                        id_ = cont[-1]
                        if id_ in self.anigameChannels:
                            self.anigameChannels.pop(id_)
                            console.print(f'👍 anigame >> {id_} - 🟥 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 anigame >> {id_} - 🟥 `")
                            dbm.setChannels("anigame",self.anigameChannels)
                        else:
                            console.print(f'🤨 anigame >> {id_} was not being sniped! ', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 anigame >> {id_} was not being sniped! `")

                    #Show Anigame Channels
                    elif m["content"] == f"{self.prefix}chans anigame":
                        if len(self.anigameChannels) == 0:
                            console.print(f'🤨 anigame >> No channels are being sniped ', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel, f"`🤨 anigame >> No channels are being sniped `")
                            return 
                        for chan in self.anigameChannels:
                            chanIDs = chan 
                            chans = self.anigameChannels[chan]
                            console.print(f'👀 anigame >> {chans} : {chanIDs} ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👀 anigame >> {chans} : {chanIDs} `")
                        

                    #Toggle Izzi Sniper 
                    elif m["content"] == f"{self.prefix}toggle izzi sniper":
                        if self.izziSniper == "on":
                            self.izziSniper = "off"
                            self.configData["izziSniper"] = "off"
                            console.print(f'👍 izzi sniper - 🟥 ', style=infoStyle, justify="left")                            
                            self.sendMessage(self.commandsChannel,"`👍 izzi sniper - 🟥 `")
                        else:
                            self.izziSniper = "on"
                            self.configData["izziSniper"] = "on"
                            console.print(f'👍 izzi sniper - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi sniper - 🟩 `")

                        dbm.setConfig(self.configData) 

                    #Toggle Izzi Hourly  
                    elif m["content"] == f"{self.prefix}toggle izzi hourly":
                        if self.izziHourly == "on":
                            self.izziHourly = "off"
                            self.configData["izziHourly"] = "off"
                            console.print(f'👍 izzi hourly - 🟥 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi hourly - 🟥 `")
                        else:
                            self.izziHourly = "on"
                            self.configData["izziHourly"] = "on"
                            try:
                                if not self.hourlyIzziThread.is_alive():
                                    self.hourlyIzziThread = self.startThread(self.hourlyIzzi)
                            except:
                                self.hourlyIzziThread = self.startThread(self.hourlyIzzi)
                            console.print(f'👍 izzi hourly - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi hourly - 🟩 `")

                        dbm.setConfig(self.configData) 

                    #Toggle Izzi Lottery 
                    elif m["content"] == f"{self.prefix}toggle izzi lottery":
                        if self.izziLottery == "on":
                            self.izziLottery = "off"
                            self.configData["izziLottery"] = "off"
                            console.print(f'👍 izzi lottery - 🟥 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi lottery - 🟥 `")
                        else:
                            self.izziLottery = "on"
                            self.configData["izziLottery"] = "on"
                            try:
                                if not self.lotteryIzziThread.is_alive():
                                    self.lotteryIzziThread = self.startThread(self.lotteryIzzi)
                            except:
                                self.lotteryIzziThread = self.startThread(self.lotteryIzzi)
                            console.print(f'👍 izzi lottery - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi lottery - 🟩 `")

                        dbm.setConfig(self.configData) 
                    
                    #Add Izzi Sniper Channel 
                    elif m["content"].startswith(f"{self.prefix}add chan izzi "):
                        cont = m["content"].split(" ")
                        name = cont[-1]
                        id_ = cont[-2]
                        if id_ not in self.izziChannels:
                            self.izziChannels[id_] = name
                            console.print(f'👍 izzi >> {name} - 🟩 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 izzi >> {name} - 🟩 `")
                            dbm.setChannels("izzi",self.izziChannels)
                        else:
                            console.print(f'🤨 izzi >> {name} is already being sniped! ', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 izzi >> {name} is already being sniped! `")

                    #Remove Izzi Sniper Channel 
                    elif m["content"].startswith(f"{self.prefix}rem chan izzi "):
                        cont = m["content"].split(" ")
                        id_ = cont[-1]
                        if id_ in self.izziChannels:
                            self.izziChannels.pop(id_)
                            console.print(f'👍 izzi >> {id_} - 🟥 ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 izzi >> {id_} - 🟥 `")
                            dbm.setChannels("izzi",self.izziChannels)
                        else:
                            console.print(f'🤨 izzi >> {id_} was not being sniped! ', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 izzi >> {id_} was not being sniped! `")

                    #Show Izzi Channels
                    elif m["content"] == f"{self.prefix}chans izzi":
                        if len(self.izziChannels) == 0:
                            console.print(f'🤨 izzi >> No channels are being sniped ', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel, f"`🤨 izzi >> No channels are being sniped `")
                            return 
                        for chan in self.izziChannels:
                            chanIDs = chan
                            chans = self.izziChannels[chan] 
                            console.print(f'👀 izzi >> {chans} : {chanIDs} ', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👀 izzi >> {chans} : {chanIDs} `")

                    #Set Latency 
                    elif m["content"].startswith(f"{self.prefix}set latency "):
                        self.latency_ = int(m["content"].split(" ")[-1])
                        self.configData["latency_"] = self.latency_
                        console.print(f'👍 latency - {self.latency_}s ', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 latency - {self.latency_}s `")

                        dbm.setConfig(self.configData) 

                    #Change Prefix
                    elif m["content"].startswith(f"{self.prefix}set prefix "):
                        self.prefix = m["content"].split(" ")[-1]
                        self.configData["prefix"] = self.prefix
                        console.print(f'👍 prefix >> \"{self.prefix}\" ', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 prefix >> \"{self.prefix}\" `")

                        dbm.setConfig(self.configData) 

                    #Settings 
                    elif m["content"] == f"{self.prefix}settings":
                        settings = f"""
`` User                - {self.user["username"]}#{self.user["discriminator"]} 
 Prefix               - {self.prefix} 
 Subgroup             - anzi 
 Tier                 - Silver 
 latency              - {"🟩" if self.latency == "on" else "🟥"} 
 latency(s)           - {self.latency_}s 
 anigame sniper       - {"🟩" if self.anigameSniper == "on" else "🟥"} 
 anigame hourly       - {"🟩" if self.anigameHourly == "on" else "🟥"} : 3610s 
 anigame lottery      - {"🟩" if self.anigameLottery == "on" else "🟥"} : 610s 
 izzi sniper          - {"🟩" if self.izziSniper == "on" else "🟥"} 
 izzi hourly          - {"🟩" if self.izziHourly == "on" else "🟥"} : 3610s 
 izzi lottery         - {"🟩" if self.izziLottery == "on" else "🟥"} : 910s ``"""
                        self.sendMessage(self.commandsChannel,settings)

                    
                    #Exit Snicord 
                    elif m["content"] == f"{self.prefix}exit":
                        console.print(f"snicord - 🟥", style=infoStyle,justify="left")
                        self.sendMessage(self.alertsChannel,"` snicord - 🟥 `")
                        self.bot.gateway.close() 

                    elif m["content"].startswith(f"{self.prefix}"):
                        console.print(f"⛔ command {m['content'].rstrip(self.prefix)} not found ", style=errorStyle,justify="left")
                        self.sendMessage(self.commandsChannel, f"`⛔ command {m['content'].rstrip(self.prefix)} not found `")

                #Anigame
                elif m["author"]["id"] == "571027211407196161":
                    #Sniper 
                    if self.anigameSniper == "on" and f"{m['channel_id']}" in self.anigameChannels:
                        if len(m["embeds"]) != 0 and m["embeds"][0]["title"] == "**What's this?**":
                            custom_id = m["components"][0]["components"][0]["custom_id"]
                            if self.latency == "on":
                                time.sleep(self.latency_)
                            self.clickButton(m["guild_id"],m["channel_id"],m["id"],custom_id,m["author"]["id"])

                        elif len(m["embeds"]) != 0 and f"Successfully claimed by __{self.user['username']}#{self.user['discriminator']}__" in m["embeds"][0]["title"]:
                            text = m["embeds"][0]["description"].replace("_","").replace("*","")
                            console.print(f"🪝  anigame >> { text } ", style=snipeStyle,justify="left")
                            if self.alerts == "on":
                                self.sendMessage(self.alertsChannel,f"`🪝 anigame >> {text} `")


                #Izzi 
                elif m["author"]["id"] == "784851074472345633":
                    #Sniper 
                    if self.izziSniper == "on" and f"{m['channel_id']}" in self.izziChannels:
                        if len(m["embeds"]) != 0 and m["embeds"][0]["title"] == "Random Card":
                            custom_id = m["components"][0]["components"][0]["custom_id"]
                            if self.latency == "on":
                                time.sleep(self.latency_)
                            self.clickButton(m["guild_id"],m["channel_id"],m["id"],custom_id,m["author"]["id"])
                        
                        elif f"has been added to **{self.user['username']}'s** collection" in m["content"]:
                            text = m["content"].replace("_","").replace("*","")
                            console.print(f"🪝  izzi >> { text } ", style=snipeStyle,justify="left")
                            if self.alerts == "on":
                                self.sendMessage(self.alertsChannel,f"`🪝 izzi >> {text} `")


        self.bot.gateway.run(auto_reconnect=True)  


    def getUserData(self,channel):
        payload = {
            "content": "` snicord - 🟩 `"
        }
        header = {
            "authorization": self.token
        }
        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", data=payload, headers=header)
        return r.json()["author"] 

    def clickButton(self,guildID,channelID,messageID,custom_id,application_id):
        headers = {
            "authorization": self.token
        }
        data = {
            "type": 3,
            "session_id": ' ',
            "guild_id": guildID,
            "channel_id": channelID,
            "message_id": messageID,
            "message_flags": 0,
            "application_id" : application_id,
            "data": {
                "component_type": 2,
                "custom_id": custom_id
                }
        }
        r = requests.post("https://discord.com/api/v9/interactions", json = data, headers = headers)
        return r

    def sendMessage(self,channel,message):
        payload = {
            "content": message
        }
        header = {
            "authorization": self.token
        }
        r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", data=payload, headers=header)
        return r 

clear()
console.rule("", style=defaultStyle)
console.print("snicord || スニコード", style=defaultStyle, justify="center")
console.print("anzi", style=defaultStyle, justify="center")
console.print("Silver", style=defaultStyle, justify="center")
console.print("Made by : Sebastian ", style=specialStyle, justify="right")

def run(token):
    sb = Selfbot(token)
    sb.run()


TOKEN = os.environ["DISCORD_TOKEN"]
run(TOKEN)