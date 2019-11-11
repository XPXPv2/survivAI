from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys


import connection.infoGrabber as infoGrabber
import connection.interacter as interacter

#class to manage the infoGrabber and the futer inteaction class
#TODO add a logging system
class connectionManager:

    def setConfig(self,obj,sub):

        attributes = dir(obj)
        for key in self.config[sub].keys():
            if not(key in attributes):
                continue
            obj.__setattr__(key,self.config[sub][key])

    def __init__(self,config):

        self.config = config

        self.grab = infoGrabber.infoGrabber()
        self.do = interacter.interacter()

        self.setConfig(self.grab,'grab')
        self.setConfig(self.do,'do')

        self.info = {}


    def initDriver(self,driver = None):
        #loads the driver
        if driver == None:
            driver = self.config['driver']

        #firefox
        if driver == 'firefox':
            options = webdriver.FirefoxOptions()
            #disables webgl to allow grabing of the screen
            options.set_preference("webgl.disabled",True)
            config = self.config["firefox_profile"]
            if config == None:
                self.driver = webdriver.Firefox(options=options)
            else:
                profile = webdriver.FirefoxProfile(config['path'])
                self.driver = webdriver.Firefox(firefox_profile=profile, options=options)

        if driver == 'chrome':
            config = self.config["chrome_profile"]
            options = webdriver.ChromeOptions()
            #disables webgl to allow grabing of the screen
            options.add_argument("--disable-webgl ")

            if config == None:
                self.driver = webdriver.Chrome(options=options)
            else:
                directory = 'user-data-dir=' + config['parentDir']
                profile = 'profile-directory=' + config['profileName']
                options.add_argument(directory)
                options.add_argument(profile)
                self.driver = webdriver.Chrome(options=options)

    def setSubDriver(self):
        self.grab.driver = self.driver
        self.do.driver = self.driver

    def updateInfo(self):
        self.info = {
        'stagnant':{'health':self.grab.get_health(),
            "tools":self.grab.get_tools(),
            'ammo':self.grab.get_ammo(),
            'healing':self.grab.get_healing(),
            'armor':self.grab.get_armour(),
            'playersAlive':self.grab.get_players_left(),
            'zoom':self.grab.get_zoom()},
        'nonstagnant':{
            'redZone':self.grab.get_red_time(),
            'image':self.grab.get_image()
            }
        }
