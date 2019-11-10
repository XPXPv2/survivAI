
import connection
import json

fp = open("config",'r')
config = json.load(fp)
fp.close()

a = connection.connectionManager.connectionManager(config)

a.initDriver()
a.setSubDriver()
a.do.loadPage()
a.do.login("botter")
