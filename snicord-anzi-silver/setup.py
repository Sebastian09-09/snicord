import dbm 
print("populating config.json")
configData = dbm.getConfig()

for i in configData:
    a = input(f"{i} : ")
    configData[i] = a

dbm.setConfig(configData)
input("press enter to continue...")