import discum
import dbm  
import requests
import os 
from rich.console import Console
console = Console()

#Styles 
defaultStyle = "bold #CD7F32"
specialStyle = "bold #4996b3"
snipeStyle = "bold #dac3a2" 

class Selfbot:
    def __init__(self,token):
        self.token = token
        #ConfigData 
        self.configData = dbm.getConfig()
        self.anigameSniper = self.configData["anigameSniper"]
        self.izziSniper = self.configData["izziSniper"]
        self.notify = self.configData["notify"]
        #SelfBot Channels 
        self.homeChannel = self.configData["homeChannel"]
        #Sniper 
        self.anigameSniper = self.configData["anigameSniper"]
        self.izziSniper = self.configData["izziSniper"]
        #Sniping Channels 
        self.channels = dbm.getChannels()
        self.anigameChannels = self.channels["anigame-channelID"]
        self.izziChannels = self.channels["izzi-channelID"] 
        #User
        self.user = self.getUserData(self.homeChannel)
        console.print(f" User     - {self.user['username']}#{self.user['discriminator']}", style=defaultStyle, justify="left")
        
    def run(self):
        self.bot = discum.Client(token=self.token, log=False)

        @self.bot.gateway.command
        def selfbot(resp):
            if resp.event.message:
                m = resp.parsed.auto() 
                #Anigame
                if m["author"]["id"] == "571027211407196161":
                    #Sniper 
                    if self.anigameSniper == "on" and f"{m['channel_id']}" in self.anigameChannels:
                        if len(m["embeds"]) != 0 and m["embeds"][0]["title"] == "**What's this?**":
                            custom_id = m["components"][0]["components"][0]["custom_id"]
                            self.clickButton(m["guild_id"],m["channel_id"],m["id"],custom_id,m["author"]["id"])

                        if len(m["embeds"]) != 0 and f"Successfully claimed by __{self.user['username']}#{self.user['discriminator']}__" in m["embeds"][0]["title"]:
                            text = m["embeds"][0]["description"].replace("_","").replace("*","")
                            console.print(f"🪝  anigame >> { text } ", style=snipeStyle,justify="left")
                            if self.notify == "on":
                                self.sendMessage(self.homeChannel,f'`🪝 anigame >> { text } `')

                #Izzi 
                if m["author"]["id"] == "784851074472345633":
                    #Sniper 
                    if self.izziSniper == "on" and f"{m['channel_id']}" in self.izziChannels:
                        if len(m["embeds"]) != 0 and m["embeds"][0]["title"] == "Random Card":
                            custom_id = m["components"][0]["components"][0]["custom_id"]
                            self.clickButton(m["guild_id"],m["channel_id"],m["id"],custom_id,m["author"]["id"])
                        
                        if f"has been added to **{self.user['username']}'s** collection" in m["content"]:
                            text = m["content"].replace("_","").replace("*","")
                            console.print(f"🪝  izzi >> { text } ", style=snipeStyle,justify="left")
                            if self.notify == "on":
                                self.sendMessage(self.homeChannel, f'`🪝 izzi >> {text} `')
        
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


console.rule("", style=defaultStyle)
console.print("snicord || スニコード", style=defaultStyle, justify="center")
console.print("anzi", style=defaultStyle, justify="center")
console.print("Bronze", style=defaultStyle, justify="center")
console.print("Made by : Sebastian ", style=specialStyle, justify="right")

def run(token):
    sb = Selfbot(token)
    sb.run()


TOKEN = os.environ["DISCORD_TOKEN"]
run(TOKEN)