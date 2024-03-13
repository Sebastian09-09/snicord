import discum
import dbm  
import requests
import time 
import threading 
import re 
import random 
import string 
import os 
from rich.console import Console
console = Console()
from dotenv import load_dotenv
load_dotenv()

from os import system, name
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

#Styles 
defaultStyle = "bold #16f3ff"
specialStyle = "bold #c9fcfe"
snipeStyle = "bold #00c9d4"
infoStyle = "bold #009aa3"
warningStyle = "bold #fc9d03"
errorStyle = "bold #fc3903"

#Keep Alive 
from flask import Flask
import logging

app = Flask('')

log = logging.getLogger('werkzeug')
log.disabled = True

@app.route('/')
def home():
    return "Snicord (anzi) platinum"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = threading.Thread(target=run)
    t.start()


class Selfbot:
    def __init__(self,token):
        self.token = token
        self.db = self.token.split(".")[1]
        #ConfigData 
        self.configData = dbm.getConfig(self.db)
        self.prefix = self.configData["prefix"]
        self.alerts = self.configData["alerts"]
        self.latency = self.configData["latency"]
        self.latency_ = int(self.configData["latency_"])
        self.controllerAccountID = self.configData["controllerAccountID"]
        self.anigameHourly = self.configData["anigameHourly"]
        self.anigameLottery = self.configData["anigameLottery"]
        self.anigameBtAll = self.configData["anigameBtAll"]
        self.anigameRdBtAll = self.configData["anigameRdBtAll"]
        self.anigameLocClearer = self.configData["anigameLocClearer"]
        self.anigamePrefix = self.configData["anigamePrefix"]
        self.izziHourly = self.configData["izziHourly"]
        self.izziLottery = self.configData["izziLottery"]
        self.izziBtAll = self.configData["izziBtAll"]
        self.izziRdBtAll = self.configData["izziRdBtAll"]
        self.izziEvBtAll = self.configData["izziEvBtAll"]
        self.izziLocClearer = self.configData["izziLocClearer"]
        self.izziPrefix = self.configData["izziPrefix"]
        #SelfBot Channels 
        self.alertsChannel = self.configData["alertsChannel"]
        self.featuresChannel = self.configData["featuresChannel"]
        self.commandsChannel = self.configData["commandsChannel"]
        #Sniper 
        self.anigameSniper = self.configData["anigameSniper"]
        self.izziSniper = self.configData["izziSniper"]
        #Sniping Channels 
        self.anigameChannels = dbm.getChannels(self.db,"anigame")
        self.izziChannels = dbm.getChannels(self.db,"izzi")
        #Rarity Alerts
        self.rarityAlerts = dbm.getAlerts(self.db)
        self.anigameRarityAlerts = self.rarityAlerts["anigame"]
        self.izziRarityAlerts = self.rarityAlerts["izzi"]
        #Intervals 
        self.intervals = dbm.getTiming(self.db)
        self.anigameHourlyInterval = self.intervals["anigameHourly"]
        self.anigameLotteryInterval = self.intervals["anigameLottery"]
        self.anigameBtAllInterval = self.intervals["anigameBtAll"]
        self.anigameRdBtAllInterval = self.intervals["anigameRdBtAll"]
        self.anigameLocClearerInterval = self.intervals["anigameLocClearer"]
        self.izziHourlyInterval = self.intervals["izziHourly"]
        self.izziLotteryInterval = self.intervals["izziLottery"]
        self.izziBtAllInterval = self.intervals["izziBtAll"]
        self.izziRdBtAllInterval = self.intervals["izziRdBtAll"]
        self.izziEvBtAllInterval = self.intervals["izziEvBtAll"]
        self.izziLocClearerInterval = self.intervals["izziLocClearer"]
        self.spamDelay = self.intervals["spamDelay"]
        #Location Clearer 
        self.goAheadAnigame = False 
        self.lostBtAnigame = False 

        self.goAheadIzzi = False 
        self.lostBtIzzi = False 

        self.Loc = dbm.getLoc(self.db)

        self.keepSpamming = dbm.getSpam(self.db)
        #User
        self.user = self.getUserData(self.alertsChannel)
        console.print(f'User     - {self.user["username"]}#{self.user["discriminator"]}\nPrefix   - {self.prefix}', style=defaultStyle, justify="left")
    
    def hourlyAnigame(self):
        while self.anigameHourly == "on":
            self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}hourly")
            time.sleep(3610)

    def lotteryAnigame(self):
        while self.anigameLottery == "on":
            time.sleep(2) #Static Pause for 2 second
            self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}lottery")
            time.sleep(610)

    def btAllAnigame(self):
        while self.anigameBtAll == "on":
            time.sleep(4) #Static Pause for 4 second
            self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}bt all")
            time.sleep(self.anigameBtAllInterval)
    
    def rdBtAllAnigame(self):
        while self.anigameRdBtAll == "on":
            time.sleep(6) #Static Pause for 6 second
            self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}rd bt all")
            time.sleep(self.anigameRdBtAllInterval)
    
    def locClearerAnigame(self):
        while self.anigameLocClearer == "on" and not self.lostBtAnigame:
            time.sleep(2)
            self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}bt")
            while self.anigameLocClearer == "on" and not self.goAheadAnigame and not self.lostBtAnigame:
                time.sleep(5) 
            self.goAheadAnigame = False 
            if not self.lostBtAnigame:
                self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}bt all")
            while self.anigameLocClearer == "on" and not self.goAheadAnigame and not self.lostBtAnigame:
                time.sleep(5)
            self.goAheadAnigame = False 
            if self.anigameLocClearer == "on" and not self.lostBtAnigame:
                self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}fl n")
                time.sleep(self.anigameLocClearerInterval)
            self.lostBtAnigame = False 


    def hourlyIzzi(self):
        while self.izziHourly == "on":
            self.sendMessage(self.featuresChannel, f"{self.izziPrefix}hourly")
            time.sleep(3610)

    def lotteryIzzi(self):
        while self.izziLottery == "on":
            time.sleep(2) #Static Pause for 2 second 
            self.sendMessage(self.featuresChannel, f"{self.izziPrefix}lottery")
            time.sleep(910) 
    
    def btAllIzzi(self):
        while self.izziBtAll == "on":
            time.sleep(4) #Static Pause for 4 second
            self.sendMessage(self.featuresChannel, f"{self.izziPrefix}bt all Hidebt")
            time.sleep(self.izziBtAllInterval)
    
    def rdBtAllIzzi(self):
        while self.izziRdBtAll == "on":
            time.sleep(6) #Static Pause for 6 second
            self.sendMessage(self.featuresChannel, f"{self.izziPrefix}rd bt all Hidebt")
            time.sleep(self.izziRdBtAllInterval) 
    
    def evBtAllIzzi(self):
        while self.evBtAllIzzi == "on":
            time.sleep(8) #Static Pause for 8 second 
            self.sendMessage(self.featuresChannel, f"{self.izziPrefix}ev bt all Hidebt")
            time.sleep(self.izziEvBtAllInterval) 
    
    def locClearerIzzi(self):
        while self.izziLocClearer == "on" and not self.lostBtIzzi:
            time.sleep(2)
            self.sendMessage(self.featuresChannel, f"{self.izziPrefix}bt Hidebt")
            while self.izziLocClearer == "on" and not self.goAheadIzzi and not self.lostBtIzzi:
                time.sleep(5) 
            self.goAheadIzzi = False 
            if not self.lostBtIzzi:
                self.sendMessage(self.featuresChannel, f"{self.izziPrefix}bt all Hidebt")
            while self.izziLocClearer == "on" and not self.goAheadIzzi and not self.lostBtIzzi:
                time.sleep(5)
            self.goAheadIzzi = False 
            if self.izziLocClearer == "on" and not self.lostBtIzzi:
                self.sendMessage(self.featuresChannel, f"{self.izziPrefix}fl n")
                time.sleep(self.izziLocClearerInterval)
            self.lostBtIzzi = False 

    def startThread(self,func):
        thr = threading.Thread(target=func, daemon=True) 
        thr.start() 
        return thr 
    
    def spam(self,channel):
        while self.keepSpamming[channel]:
            res = ''.join(random.choices(string.ascii_letters, k=random.randint(5,30)))
            self.sendMessage(channel,res) 
            time.sleep(self.spamDelay)
        self.keepSpamming.pop(channel) 

        dbm.setSpam(self.db,self.keepSpamming)

    def startSpam(self,channel):
        thr = threading.Thread(target=self.spam, daemon=True , args=(channel,))
        thr.start()
        return thr 
        
    def run(self):
        self.bot = discum.Client(token=self.token, log=False)

        @self.bot.gateway.command
        def selfbot(resp):
            if resp.event.message:
                m = resp.parsed.auto() 
                #Say Command 
                if m["author"]["id"] == self.controllerAccountID and m["content"].startswith(f"{self.prefix}say "):
                        cmd = " ".join(m["content"].split("say")[1:])
                        self.sendMessage(m["channel_id"],cmd)

                #Commands 
                if m["author"]["id"] == self.user["id"] and m['channel_id'] == self.commandsChannel or m["author"]["id"] == self.controllerAccountID and m['channel_id'] == self.commandsChannel:
                    #Say
                    if m["content"].startswith(f"{self.prefix}say "):
                        return 
                    
                    #Toggle Latency 
                    elif m["content"] == f"{self.prefix}toggle latency":
                        if self.latency == "on":
                            self.latency = "off"
                            self.configData["latency"] = "off"
                            console.print(f'👍 latency - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 latency - 🟥 `")
                        else:
                            self.latency = "on"
                            self.configData["latency"] = "on"
                            console.print(f'👍 latency - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 latency - 🟩 `")

                        dbm.setConfig(self.db,self.configData)

                    #Set Latency 
                    elif m["content"].startswith(f"{self.prefix}set latency "):
                        self.latency_ = int(m["content"].split(" ")[-1])
                        self.configData["latency_"] = self.latency_
                        console.print(f'👍 latency - {self.latency_}s << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 latency - {self.latency_}s `")

                        dbm.setConfig(self.db,self.configData) 
                    
                    #Toggle Alerts 
                    elif m["content"] == f"{self.prefix}toggle alerts":
                        if self.alerts == "on":
                            self.alerts = "off"
                            self.configData["alerts"] = "off"
                            console.print(f'👍 alerts - 🟥  << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 alerts - 🟥 `")
                        else:
                            self.alerts = "on"
                            self.configData["alerts"] = "on"
                            console.print(f'👍 alerts - 🟩  << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 alerts - 🟩 `")

                        dbm.setConfig(self.configData) 
                    
                    #Spam
                    elif m["content"].startswith(f"{self.prefix}spam "):
                        channel = m["content"].split(" ")[-1]
                        if channel in self.keepSpamming and self.keepSpamming[channel][0] == True:
                            console.print(f'🤨 channel already being spammed << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 channel already being spammed `")
                            return
                        self.keepSpamming[channel] = True
                        self.startSpam(channel)
                        console.print(f'👍 spamming in channel - {channel} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 spamming in channel - {channel} `")

                        dbm.setSpam(self.db,self.keepSpamming)
                    
                    #Stop Spam
                    elif m["content"].startswith(f"{self.prefix}stop spam "):
                        channel = m["content"].split(" ")[-1]
                        if channel not in self.keepSpamming:
                            console.print(f'🤨 channel not being spammed << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 channel not being spammed `")
                            return 
                        if self.keepSpamming[channel] == False:
                            console.print(f'🤨 channel not being spammed << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 channel not being spammed `")
                            return 
                        self.keepSpamming[channel] = False
                        console.print(f'👍 stopped spamming in channel - {channel} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 stopped spamming in channel - {channel} `")

                        dbm.setSpam(self.db,self.keepSpamming)
                    
                    #Set Spam 
                    elif m["content"].startswith(f"{self.prefix}set spam "):
                        self.spamDelay = int(m["content"].split(" ")[-1])
                        self.intervals["spamDelay"] = self.spamDelay
                        console.print(f'👍 spam delay - {self.spamDelay}s << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 spam delay - {self.spamDelay}s `")

                        dbm.setTiming(self.db,self.intervals)

                    #Toggle Anigame Sniper 
                    elif m["content"] == f"{self.prefix}toggle anigame sniper":
                        if self.anigameSniper == "on":
                            self.anigameSniper = "off"
                            self.configData["anigameSniper"] = "off"
                            console.print(f'👍 anigame sniper - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame sniper - 🟥 `")
                        else:
                            self.anigameSniper = "on"
                            self.configData["anigameSniper"] = "on"
                            console.print(f'👍 anigame sniper - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame sniper - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Anigame Hourly 
                    elif m["content"] == f"{self.prefix}toggle anigame hourly":
                        if self.anigameHourly == "on":
                            self.anigameHourly = "off"
                            self.configData["anigameHourly"] = "off"
                            console.print(f'👍 anigame hourly - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame hourly - 🟥 `")
                        else:
                            self.anigameHourly = "on"
                            self.configData["anigameHourly"] = "on"
                            try:
                                if not self.hourlyAnigameThread.is_alive():
                                    self.hourlyAnigameThread = self.startThread(self.hourlyAnigame) 
                            except AttributeError:
                                self.hourlyAnigameThread = self.startThread(self.hourlyAnigame)
                            console.print(f'👍 anigame hourly - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame hourly - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Anigame Lottery 
                    elif m["content"] == f"{self.prefix}toggle anigame lottery":
                        if self.anigameLottery == "on":
                            self.anigameLottery = "off"
                            self.configData["anigameLottery"] = "off"
                            console.print(f'👍 anigame lottery - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame lottery - 🟥 `")
                        else:
                            self.anigameLottery = "on"
                            self.configData["anigameLottery"] = "on"
                            try:
                                if not self.lotteryAnigameThread.is_alive():
                                    self.lotteryAnigameThread = self.startThread(self.lotteryAnigame)
                            except AttributeError:
                                self.lotteryAnigameThread = self.startThread(self.lotteryAnigame)
                            console.print(f'👍 anigame lottery - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame lottery - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Anigame Bt all 
                    elif m["content"] == f"{self.prefix}toggle anigame bt all":
                        if self.anigameBtAll == "on":
                            self.anigameBtAll = "off"
                            self.configData["anigameBtAll"] = "off"
                            console.print(f'👍 anigame bt all - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame bt all - 🟥 `")
                        else:
                            self.anigameBtAll = "on"
                            self.configData["anigameBtAll"] = "on"
                            try:
                                if not self.btAllAnigameThread.is_alive():
                                    self.btAllAnigameThread = self.startThread(self.btAllAnigame)
                            except AttributeError:
                                self.btAllAnigameThread = self.startThread(self.btAllAnigame)
                            console.print(f'👍 anigame bt all - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame bt all - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Anigame Rd Bt all 
                    elif m["content"] == f"{self.prefix}toggle anigame rd bt all":
                        if self.anigameRdBtAll == "on":
                            self.anigameRdBtAll = "off"
                            self.configData["anigameRdBtAll"] = "off"
                            console.print(f'👍 anigame rd bt all - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame rd bt all - 🟥 `")
                        else:
                            self.anigameRdBtAll = "on"
                            self.configData["anigameRdBtAll"] = "on"
                            try:
                                if not self.rdBtAllAnigameThread.is_alive():
                                    self.rdBtAllAnigameThread = self.startThread(self.rdBtAllAnigame)
                            except AttributeError:
                                self.rdBtAllAnigameThread = self.startThread(self.rdBtAllAnigame)
                            console.print(f'👍 anigame rd bt all - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame rd bt all - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Anigame Loc Clearer
                    elif m["content"] == f"{self.prefix}toggle anigame loc cl":
                        if self.anigameLocClearer == "on":
                            self.anigameLocClearer = "off"
                            self.configData["anigameLocClearer"] = "off"
                            console.print(f'👍 anigame loc clearer - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame loc clearer - 🟥 `")
                        else:
                            self.anigameLocClearer = "on"
                            self.configData["anigameLocClearer"] = "on"
                            try:
                                if not self.locClearerAnigameThread.is_alive():
                                    self.locClearerAnigameThread = self.startThread(self.locClearerAnigame)
                            except AttributeError:
                                self.locClearerAnigameThread = self.startThread(self.locClearerAnigame)
                            console.print(f'👍 anigame loc clearer - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 anigame loc clearer - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 


                    #Add Anigame Sniper Channel 
                    elif m["content"].startswith(f"{self.prefix}add chan anigame "):
                        cont = m["content"].split(" ")
                        name = cont[-1]
                        id_ = cont[-2]
                        if id_ not in self.anigameChannels:
                            self.anigameChannels[id_] = name
                            console.print(f'👍 {name} - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 {name} - 🟩 `")
                            dbm.setChannels(self.db,"anigame",self.anigameChannels)
                        else:
                            console.print(f'🤨 {name} is already being sniped! << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 {name} is already being sniped! `")

                    #Remove Anigame Sniper Channel 
                    elif m["content"].startswith(f"{self.prefix}rem chan anigame "):
                        cont = m["content"].split(" ")
                        id_ = cont[-1]
                        if id_ in self.anigameChannels:
                            self.anigameChannels.pop(id_)
                            console.print(f'👍 {id_} - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 {id_} - 🟥 `")
                            dbm.setChannels(self.db,"anigame",self.anigameChannels)
                        else:
                            console.print(f'🤨 {id_} was not being sniped! << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 {id_} was not being sniped! `")

                    #Show Anigame Channels
                    elif m["content"] == f"{self.prefix}chans anigame":
                        if len(self.anigameChannels) == 0:
                            console.print(f'🤨 No channels are being sniped << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel, f"`🤨 No channels are being sniped `")
                            return 
                        for chan in self.anigameChannels:
                            chanIDs = chan 
                            chans = self.anigameChannels[chan]
                            console.print(f'👀 anigame >> {chans} : {chanIDs} << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👀 anigame >> {chans} : {chanIDs} `")
                        


                    #Toggle Izzi Sniper 
                    elif m["content"] == f"{self.prefix}toggle izzi sniper":
                        if self.izziSniper == "on":
                            self.izziSniper = "off"
                            self.configData["izziSniper"] = "off"
                            console.print(f'👍 izzi sniper - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi sniper - 🟥 `")
                        else:
                            self.izziSniper = "on"
                            self.configData["izziSniper"] = "on"
                            console.print(f'👍 izzi sniper - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi sniper - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Izzi Hourly  
                    elif m["content"] == f"{self.prefix}toggle izzi hourly":
                        if self.izziHourly == "on":
                            self.izziHourly = "off"
                            self.configData["izziHourly"] = "off"
                            console.print(f'👍 izzi hourly - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi hourly - 🟥 `")
                        else:
                            self.izziHourly = "on"
                            self.configData["izziHourly"] = "on"
                            try:
                                if not self.hourlyIzziThread.is_alive():
                                    self.hourlyIzziThread = self.startThread(self.hourlyIzzi)
                            except:
                                self.hourlyIzziThread = self.startThread(self.hourlyIzzi)
                            console.print(f'👍 izzi hourly - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi hourly - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Izzi Lottery 
                    elif m["content"] == f"{self.prefix}toggle izzi lottery":
                        if self.izziLottery == "on":
                            self.izziLottery = "off"
                            self.configData["izziLottery"] = "off"
                            console.print(f'👍 izzi lottery - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi lottery - 🟥 `")
                        else:
                            self.izziLottery = "on"
                            self.configData["izziLottery"] = "on"
                            try:
                                if not self.lotteryIzziThread.is_alive():
                                    self.lotteryIzziThread = self.startThread(self.lotteryIzzi)
                            except:
                                self.lotteryIzziThread = self.startThread(self.lotteryIzzi)
                            console.print(f'👍 izzi lottery - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi lottery - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Izzi Bt all 
                    elif m["content"] == f"{self.prefix}toggle izzi bt all":
                        if self.izziBtAll == "on":
                            self.izziBtAll = "off"
                            self.configData["izziBtAll"] = "off"
                            console.print(f'👍 izzi bt all - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi bt all - 🟥 `")
                        else:
                            self.izziBtAll = "on"
                            self.configData["izziBtAll"] = "on"
                            try:
                                if not self.btAllIzziThread.is_alive():
                                    self.btAllIzziThread = self.startThread(self.btAllIzzi)
                            except AttributeError:
                                self.btAllIzziThread = self.startThread(self.btAllIzzi)
                            console.print(f'👍 izzi bt all - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi bt all - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Izzi Rd Bt all 
                    elif m["content"] == f"{self.prefix}toggle izzi rd bt all":
                        if self.izziRdBtAll == "on":
                            self.izziRdBtAll = "off"
                            self.configData["izziRdBtAll"] = "off"
                            console.print(f'👍 izzi rd bt all - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi rd bt all - 🟥 `")
                        else:
                            self.izziRdBtAll = "on"
                            self.configData["izziRdBtAll"] = "on"
                            try:
                                if not self.rdBtAllIzziThread.is_alive():
                                    self.rdBtAllIzziThread = self.startThread(self.rdBtAllIzzi)
                            except AttributeError:
                                self.rdBtAllIzziThread = self.startThread(self.rdBtAllIzzi)
                            console.print(f'👍 izzi rd bt all - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi rd bt all - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Izzi Ev Bt all 
                    elif m["content"] == f"{self.prefix}toggle izzi ev bt all":
                        if self.izziEvBtAll == "on":
                            self.izziEvBtAll = "off"
                            self.configData["izziEvBtAll"] = "off"
                            console.print(f'👍 izzi ev bt all - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi ev bt all - 🟥 `")
                        else:
                            self.izziEvBtAll = "on"
                            self.configData["izziEvBtAll"] = "on"
                            try:
                                if not self.evBtAllIzziThread.is_alive():
                                    self.evBtAllIzziThread = self.startThread(self.evBtAllIzzi)
                            except AttributeError:
                                self.evBtAllIzziThread = self.startThread(self.evBtAllIzzi)
                            console.print(f'👍 izzi ev bt all - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi ev bt all - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    #Toggle Izzi Loc Clearer
                    elif m["content"] == f"{self.prefix}toggle izzi loc cl":
                        if self.izziLocClearer == "on":
                            self.izziLocClearer = "off"
                            self.configData["izziLocClearer"] = "off"
                            console.print(f'👍 izzi loc clearer - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi loc clearer - 🟥 `")
                        else:
                            self.izziLocClearer = "on"
                            self.configData["izziLocClearer"] = "on"
                            try:
                                if not self.locClearerIzziThread.is_alive():
                                    self.locClearerIzziThread = self.startThread(self.locClearerIzzi)
                            except AttributeError:
                                self.locClearerIzziThread = self.startThread(self.locClearerIzzi)
                            console.print(f'👍 izzi loc clearer - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,"`👍 izzi loc clearer - 🟩 `")

                        dbm.setConfig(self.db,self.configData) 

                    
                    #Add Izzi Sniper Channel 
                    elif m["content"].startswith(f"{self.prefix}add chan izzi "):
                        cont = m["content"].split(" ")
                        name = cont[-1]
                        id_ = cont[-2]
                        if id_ not in self.izziChannels:
                            self.izziChannels[id_] = name
                            console.print(f'👍 {name} - 🟩 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 {name} - 🟩 `")
                            dbm.setChannels(self.db,"izzi",self.izziChannels)
                        else:
                            console.print(f'🤨 {name} is already being sniped! << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 {name} is already being sniped! `")

                    #Remove Izzi Sniper Channel 
                    elif m["content"].startswith(f"{self.prefix}rem chan izzi "):
                        cont = m["content"].split(" ")
                        id_ = cont[-1]
                        if id_ in self.izziChannels:
                            self.izziChannels.pop(id_)
                            console.print(f'👍 {id_} - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 {id_} - 🟥 `")
                            dbm.setChannels(self.db,"izzi",self.izziChannels)
                        else:
                            console.print(f'🤨 {id_} was not being sniped! << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 {id_} was not being sniped! `")

                    #Show Izzi Channels
                    elif m["content"] == f"{self.prefix}chans izzi":
                        if len(self.izziChannels) == 0:
                            console.print(f'🤨 No channels are being sniped << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel, f"`🤨 No channels are being sniped `")
                            return 
                        for chan in self.izziChannels:
                            chanIDs = chan
                            chans = self.izziChannels[chan] 
                            console.print(f'👀 izzi >> {chans} : {chanIDs} << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👀 izzi >> {chans} : {chanIDs} `") 

                    #Change Prefix
                    elif m["content"].startswith(f"{self.prefix}set prefix "):
                        self.prefix = m["content"].split(" ")[-1]
                        self.configData["prefix"] = self.prefix
                        console.print(f'👍 prefix >> \"{self.prefix}\" << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 prefix >> \"{self.prefix}\" `")

                        dbm.setConfig(self.db,self.configData) 

                    #Change Timing Anigame Hourly 
                    elif m["content"].startswith(f"{self.prefix}set anigame hourly interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.anigameHourlyInterval = timing
                        self.intervals["anigameHourly"] = self.anigameHourlyInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for anigame hourly - {self.anigameHourlyInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for anigame hourly - {self.anigameHourlyInterval} `")

                    #Change Timing Anigame Lottery 
                    elif m["content"].startswith(f"{self.prefix}set anigame lottery interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.anigameLotteryInterval = timing
                        self.intervals["anigameLottery"] = self.anigameLotteryInterval
                        dbm.setTiming(self.db,self.intervals) 
                        console.print(f'👍 new interval for anigame lottery - {self.anigameLotteryInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for anigame lottery - {self.anigameLotteryInterval} `")

                    #Change Timing Anigame Bt All 
                    elif m["content"].startswith(f"{self.prefix}set anigame bt all interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.anigameBtAllInterval = timing
                        self.intervals["anigameBtAll"] = self.anigameBtAllInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for anigame bt all - {self.anigameBtAllInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for anigame bt all - {self.anigameBtAllInterval} `") 
                    
                    #Change Timing Anigame Rd Bt All 
                    elif m["content"].startswith(f"{self.prefix}set anigame rd bt all interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.anigameRdBtAllInterval = timing
                        self.intervals["anigameRdBtAll"] = self.anigameRdBtAllInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for anigame rd bt all - {self.anigameRdBtAllInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for anigame rd bt all - {self.anigameRdBtAllInterval} `") 
                    
                    #Change Timing Anigame Loc Clearer  
                    elif m["content"].startswith(f"{self.prefix}set anigame loc cl interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.anigameLocClearerInterval = timing
                        self.intervals["anigameLocClearer"] = self.anigameLocClearerInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for anigame loc clearer - {self.anigameLocClearerInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for anigame loc clearer - {self.anigameLocClearerInterval} `") 


                    #Change Timing Izzi Hourly 
                    elif m["content"].startswith(f"{self.prefix}set izzi hourly interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.izziHourlyInterval = timing
                        self.intervals["izziHourly"] = self.izziHourlyInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for izzi hourly - {self.izziHourlyInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for izzi hourly - {self.izziHourlyInterval} `")

                    #Change Timing Izzi Lottery 
                    elif m["content"].startswith(f"{self.prefix}set izzi lottery interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.izziLotteryInterval = timing
                        self.intervals["izziLottery"] = self.izziLotteryInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for izzi lottery - {self.izziLotteryInterval} ', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for izzi lottery - {self.izziLotteryInterval} `")

                    #Change Timing Izzi Bt All 
                    elif m["content"].startswith(f"{self.prefix}set izzi bt all interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.izziBtAllInterval = timing
                        self.intervals["izziBtAll"] = self.izziBtAllInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for izzi bt all - {self.izziBtAllInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for izzi bt all - {self.izziBtAllInterval} `")

                    #Change Timing Izzi Rd Bt All 
                    elif m["content"].startswith(f"{self.prefix}set izzi rd bt all interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.izziRdBtAllInterval = timing
                        self.intervals["izziRdBtAll"] = self.izziRdBtAllInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for izzi rd bt all - {self.izziRdBtAllInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for izzi rd bt all - {self.izziRdBtAllInterval} `")

                    #Change Timing Izzi Ev Bt All 
                    elif m["content"].startswith(f"{self.prefix}set izzi ev bt all interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.izziEvBtAllInterval = timing
                        self.intervals["izziEvBtAll"] = self.izziEvBtAllInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for izzi ev bt all - {self.izziEvBtAllInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for izzi ev bt all - {self.izziEvBtAllInterval} `")

                    #Change Timing Izzi Loc Clearer 
                    elif m["content"].startswith(f"{self.prefix}set izzi loc cl interval "):
                        timing = int(m["content"].split(" ")[-1])
                        self.izziLocClearerInterval = timing
                        self.intervals["izziLocClearer"] = self.izziLocClearerInterval
                        dbm.setTiming(self.db, self.intervals) 
                        console.print(f'👍 new interval for izzi loc clearer - {self.izziLocClearerInterval} << {self.user["username"]}', style=infoStyle, justify="left")
                        self.sendMessage(self.commandsChannel,f"`👍 new interval for izzi loc clearer - {self.izziLocClearerInterval} `")
                    
                    #Add Alerts Anigame 
                    elif m["content"].startswith(f"{self.prefix}add alert anigame "):
                        alert = m["content"].split(" ")[-1].lower()
                        if alert not in self.anigameRarityAlerts:
                            self.anigameRarityAlerts.append(alert)
                            self.rarityAlerts["anigame"] = self.anigameRarityAlerts
                            dbm.setAlerts(self.db, self.rarityAlerts)
                            console.print(f'👍 anigame >> new alert for \"{alert}\" set up << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 anigame >> new alert for \"{alert}\" set up `")
                        else:
                            console.print(f'🤨 anigame >> alert already set for \"{alert}\" << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 anigame >> alert already set for \"{alert}\" `")

                    #Rem Alerts Anigame 
                    elif m["content"].startswith(f"{self.prefix}rem alert anigame "):
                        alert = m["content"].split(" ")[-1].lower()
                        if alert in self.anigameRarityAlerts:
                            self.anigameRarityAlerts.remove(alert)
                            self.rarityAlerts["anigame"] = self.anigameRarityAlerts
                            dbm.setAlerts(self.db, self.rarityAlerts)
                            console.print(f'👍 anigame >> removed alert for \"{alert}\" << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 anigame >> removed alert for \"{alert}\" `")
                        else:
                            console.print(f'🤨 anigame >> no alert for \"{alert}\" << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 anigame >> no alert for \"{alert}\" `")

                    #Add Alerts Izzi 
                    elif m["content"].startswith(f"{self.prefix}add alert izzi "):
                        alert = m["content"].split(" ")[-1].lower()
                        if alert not in self.izziRarityAlerts:
                            self.izziRarityAlerts.append(alert)
                            self.rarityAlerts["izzi"] = self.izziRarityAlerts
                            dbm.setAlerts(self.db, self.rarityAlerts)
                            console.print(f'👍 izzi >> new alert for \"{alert}\" set up << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 izzi >> new alert for \"{alert}\" set up `")
                        else:
                            console.print(f'🤨 izzi >> alert already set for \"{alert}\" << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 izzi >> alert already set for \"{alert}\" `")

                    #Rem Alerts Izzi 
                    elif m["content"].startswith(f"{self.prefix}rem alert izzi "):
                        alert = m["content"].split(" ")[-1].lower()
                        if alert in self.izziRarityAlerts:
                            self.izziRarityAlerts.remove(alert)
                            self.rarityAlerts["izzi"] = self.izziRarityAlerts
                            dbm.setAlerts(self.db, self.rarityAlerts)
                            console.print(f'👍 izzi >> removed alert for \"{alert}\" << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`👍 izzi >> removed alert for \"{alert}\" `")
                        else:
                            console.print(f'🤨 izzi >> no alert for \"{alert}\" << {self.user["username"]}', style=warningStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🤨 izzi >> no alert for \"{alert}\" `")
                    
                    #Show Alerts 
                    elif m["content"] == f"{self.prefix}alerts":
                        for i in self.anigameRarityAlerts:
                            console.print(f'🔔 anigame >> {i} << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🔔 anigame >> {i} `")
                        for i in self.izziRarityAlerts:
                            console.print(f'🔔 izzi >> {i} << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.commandsChannel,f"`🔔 izzi >> {i} `")

                    #Settings 
                    elif m["content"] == f"{self.prefix}settings":
                        settings = f"""
`` User                - {self.user["username"]}#{self.user["discriminator"]} 
 Prefix               - {self.prefix} 
 Subgroup             - anzi 
 Tier                 - Platinum 
 latency              - {"🟩" if self.latency == "on" else "🟥"} 
 latency(s)           - {self.latency_}s 
 anigame sniper       - {"🟩" if self.anigameSniper == "on" else "🟥"} 
 anigame hourly       - {"🟩" if self.anigameHourly == "on" else "🟥"} : {self.anigameHourlyInterval}s 
 anigame lottery      - {"🟩" if self.anigameLottery == "on" else "🟥"} : {self.anigameLotteryInterval}s 
 anigame bt all       - {"🟩" if self.anigameBtAll == "on" else "🟥"} : {self.anigameBtAllInterval}s 
 anigame rd bt all    - {"🟩" if self.anigameRdBtAll == "on" else "🟥"} : {self.anigameRdBtAllInterval}s 
 anigame loc clearer  - {"🟩" if self.anigameLocClearer == "on" else "🟥"} : {self.anigameLocClearerInterval}s 
 izzi sniper          - {"🟩" if self.izziSniper == "on" else "🟥"} 
 izzi hourly          - {"🟩" if self.izziHourly == "on" else "🟥"} : {self.izziHourlyInterval}s 
 izzi lottery         - {"🟩" if self.izziLottery == "on" else "🟥"} : {self.izziLotteryInterval}s 
 izzi bt all          - {"🟩" if self.izziBtAll == "on" else "🟥"} : {self.izziBtAllInterval}s 
 izzi rd bt all       - {"🟩" if self.izziRdBtAll == "on" else "🟥"} : {self.izziRdBtAllInterval}s 
 izzi ev bt all       - {"🟩" if self.izziEvBtAll == "on" else "🟥"} : {self.izziEvBtAllInterval}s 
 izzi loc clearer     - {"🟩" if self.izziLocClearer == "on" else "🟥"} : {self.izziLocClearerInterval}s ``"""
                        self.sendMessage(self.commandsChannel,settings)

                    
                    #Exit Snicord 
                    elif m["content"] == f"{self.prefix}exit":
                        console.print(f'snicord - 🟥 << {self.user["username"]}', style=infoStyle, justify="left")
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
                            console.print(f'🪝  anigame >> {text} << {self.user["username"]}', style=snipeStyle, justify="left")
                            rarity = re.findall("__.+__", m["embeds"][0]["description"])[0].strip("__").lower()
                            if self.alerts == "on":
                                if rarity in self.anigameRarityAlerts:
                                    self.sendMessage(self.alertsChannel,f"`🪝 anigame >> {text} ` <@{self.controllerAccountID}>")
                                    self.makeUnread(self.alertsChannel)
                                else:
                                    self.sendMessage(self.alertsChannel,f"`🪝 anigame >> {text} `")
                    #Bt Anigame
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f" Challenging Area " in m["embeds"][0]["title"]:
                        custom_id = m["components"][0]["components"][0]["custom_id"]
                        self.clickButton(m["guild_id"],m["channel_id"],m["id"],custom_id,m["author"]["id"])
                    
                    #Change State Bt/Bt all Anigame 
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f"**Victory" in m["embeds"][0]["title"] and self.user["username"] in m["embeds"][0]["author"]["name"]:
                        self.goAheadAnigame = True 
                    
                    #Lost Anigame Bt/Bt all
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f"**Defeated" in m["embeds"][0]["title"] and self.user["username"] in m["embeds"][0]["author"]["name"]:
                        self.lostBtAnigame = True 
                        self.anigameLocClearer = "off"
                        console.print(f"😭 anigame >> Deafeated in Battle Location : {self.Loc['anigame'][0]}  Floor : {self.Loc['anigame'][1]} << {self.user['username']}", style=infoStyle, justify="left")
                        self.sendMessage(self.alertsChannel , f"`😭 anigame >> Deafeated in Battle Location : {self.Loc['anigame'][0]}  Floor : {self.Loc['anigame'][1]} ` <@{self.controllerAccountID}>" )
                        self.makeUnread(self.alertsChannel)

                    #Change Location 
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f"Error" in m["embeds"][0]["title"] and self.user["username"] in m["embeds"][0]["author"]["name"] and "this floor is not accessible!" in m["embeds"][0]["description"]:
                        loc=int(self.Loc["anigame"][0])
                        self.Loc["anigame"][0] = str(loc+1)
                        self.Loc["anigame"][1] = "1"  
                        self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}loc {self.Loc['anigame'][0]}")

                        dbm.setLoc(self.db,self.Loc)

                    #Read Location/Floor 
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f"Travelled to Area" in m["embeds"][0]["title"] and self.user["username"] in m["embeds"][0]["author"]["name"]:
                        dat = m["embeds"][0]["title"].split("[")[-1].split("]")[0].strip("**").split("-")
                        self.Loc["anigame"][0] = dat[0].strip()
                        self.Loc["anigame"][1] = dat[1].strip()

                        dbm.setLoc(self.db,self.Loc)
                    
                    #No Stamina 
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f"Error" in m["embeds"][0]["title"] and self.user["username"] in m["embeds"][0]["author"]["name"]:
                        if "You do not have enough stamina to proceed!" in m["embeds"][0]["description"] or "Summoner, you must fight at least once!" in m["embeds"][0]["description"]:
                            console.print(f'😪 anigame >> No Stamina for Battle waiting for {self.anigameLocClearerInterval}s << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.alertsChannel , f"`😪 anigame >> No Stamina for Battle waiting for {self.anigameLocClearerInterval}s `")
                            time.sleep(self.anigameLocClearerInterval)

                            self.locClearerAnigameThread = self.startThread(self.locClearerAnigame)



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
                            console.print(f'🪝  izzi >> {text} << {self.user["username"]}', style=snipeStyle, justify="left")
                            rarity = re.findall("__.+__", m["content"])[0].strip("__").lower()
                            if self.alerts == "on":
                                if rarity in self.izziRarityAlerts:
                                    self.sendMessage(self.alertsChannel,f"`🪝 izzi >> {text} ` <@{self.controllerAccountID}>")
                                    self.makeUnread(self.alertsChannel)
                                else:
                                    self.sendMessage(self.alertsChannel,f"`🪝 izzi >> {text} `")
                    
                    #Change State Bt/Bt all Izzi 
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f"Victory" in m["embeds"][0]["title"] and self.user["username"] in m["embeds"][0]["author"]["name"]:
                        self.goAheadIzzi = True

                    #Lost Izzi Bt/Bt all
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f"Defeated" in m["embeds"][0]["title"] and self.user["username"] in m["embeds"][0]["author"]["name"]:
                        self.lostBtIzzi = True 
                        self.izziLocClearer = "off"
                        console.print(f"😭 izzi >> Deafeated in Battle Location : {self.Loc['izzi'][0]}  Floor : {self.Loc['izzi'][1]} << {self.user['username']}", style=infoStyle, justify="left")
                        self.sendMessage(self.alertsChannel , f"`😭 izzi >> Deafeated in Battle Location : {self.Loc['izzi'][0]}  Floor : {self.Loc['izzi'][1]} ` <@{self.controllerAccountID}>" )
                        self.makeUnread(self.alertsChannel)

                    #Change Location 
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) == 0 and f"Summoner **{self.user['username']}**, you have cleared this zone!" in m["content"]:
                        loc=int(self.Loc["izzi"][0])
                        self.Loc["izzi"][0] = str(loc+1)
                        self.Loc["izzi"][1] = "1"
                        self.sendMessage(self.featuresChannel, f"{self.anigamePrefix}zone n")

                        dbm.setLoc(self.db,self.Loc)

                    #Read Location/Floor 
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f"Travelled to Arena" in m["embeds"][0]["title"] and self.user["username"] in m["embeds"][0]["author"]["name"]:
                        dat = m["embeds"][0]["title"].split("[")[-1].split("]")[0].split("-")
                        self.Loc["izzi"][0] = dat[0].strip()
                        self.Loc["izzi"][1] = dat[1].strip()

                        dbm.setLoc(self.db,self.Loc)
                    
                    #No Stamina 
                    if m['channel_id'] == self.featuresChannel and len(m["embeds"]) != 0 and f"Error" in m["embeds"][0]["title"] and self.user["username"] in m["embeds"][0]["author"]["name"]:
                        if "You do not have enough mana to proceed!" in m["embeds"][0]["description"]:
                            console.print(f'😪 izzi >> No Stamina for Battle waiting for {self.izziLocClearerInterval}s << {self.user["username"]}', style=infoStyle, justify="left")
                            self.sendMessage(self.alertsChannel , f"`😪 izzi >> No Stamina for Battle waiting for {self.izziLocClearerInterval}s `")
                            time.sleep(self.izziLocClearerInterval)

                            self.locClearerIzziThread = self.startThread(self.locClearerIzzi)
                    

        if self.anigameHourly == "on":
            self.hourlyAnigameThread = self.startThread(self.hourlyAnigame)

        if self.anigameLottery == "on":
            self.lotteryAnigameThread = self.startThread(self.lotteryAnigame)
        
        if self.anigameBtAll == "on":
            self.btAllAnigameThread = self.startThread(self.btAllAnigame)
        
        if self.anigameRdBtAll == "on":
            self.rdBtAllAnigameThread = self.startThread(self.rdBtAllAnigame)
        
        if self.anigameLocClearer == "on":
            self.locClearerAnigameThread = self.startThread(self.locClearerAnigame)
            
        if self.izziHourly == "on":
            self.hourlyIzziThread = self.startThread(self.hourlyIzzi)

        if self.izziLottery == "on":
            self.lotteryIzziThread = self.startThread(self.lotteryIzzi)
        
        if self.izziBtAll == "on":
            self.btAllIzziThread = self.startThread(self.btAllIzzi)
        
        if self.izziRdBtAll == "on":
            self.rdBtAllIzziThread = self.startThread(self.rdBtAllIzzi)
        
        if self.izziEvBtAll == "on":
            self.evBtAllIzziThread = self.startThread(self.evBtAllIzzi)
        
        if self.izziLocClearer == "on":
            self.locClearerIzziThread = self.startThread(self.locClearerIzzi)
        
        for i in self.keepSpamming:
            if self.keepSpamming[i] == True:
                self.startSpam(i)

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
    
    def makeUnread(self,channelID):
        headers = {
            'authorization' : self.token
        }
        r = requests.get(f'https://discord.com/api/v9/channels/{channelID}/messages?limit=2' , headers=headers)
        jsondat = r.json() 
        messageID = jsondat[-1].get('id')
        url = f'https://discord.com/api/v9/channels/{channelID}/messages/{messageID}/ack'
        r = requests.post(url , headers={"authorization":self.token} , json={"manual":True , "mention_count":1})
        return(r.status_code) 


def runSnicord(token):
    sb = Selfbot(token)
    sb.run()

keep_alive()
clear()
console.rule("", style=defaultStyle)
console.print("snicord || スニコード", style=defaultStyle, justify="center")
console.print("anzi", style=defaultStyle, justify="center")
console.print("Platinum", style=defaultStyle, justify="center")
console.print("Made by : Sebastian ", style=specialStyle, justify="right")
for i in os.environ:
    if i.startswith("DISCORD_TOKEN"):
        TOKEN = os.getenv(i)
        sbThread = threading.Thread(target=runSnicord, args=(TOKEN,))    
        sbThread.start()