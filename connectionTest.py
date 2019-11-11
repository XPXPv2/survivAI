
import connection
import json
import time

fp = open("config",'r')
config = json.load(fp)
fp.close()

a = connection.connectionManager.connectionManager(config)

a.initDriver()
a.setSubDriver()
a.do.loadPage()
a.do.login("botter")
time.sleep(10)
a.updateInfo()
print(a.info)
while(True):
    """
    #auto healing
    for item in a.info['stagnant']['healing'].keys():
        a.do.useHealing(item)
    """
    pass
