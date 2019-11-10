
import infoGrabber
import interacter

#class to manage the infoGrabber and the futer inteaction class
#TODO implument the class
#TODO add a logging system
#TODO replace with CSD/json file for all config insted of seperate files to make more orginized

class connectionManager:

    def setConfig(self,obj):

        attributes = dir(obj)
        for key in self.config.keys():
            if not(key in attributes):
                continue
            obj.__setattr__(key,self.config[key])

    def __init__(self,config):

        self.config = config

        self.grabber = infoGrabber.infoGrabber()

        self.setConfig(self.grabber)

        print(self.grabber.FAILED_HEALTH)

    def initDriver(self,brower = 'firefox'):
        #loads the driver

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
                directory = 'user-data-dir=' + config['homeDir']
                profile = 'profile-directory=' + config['profileDir']
                options.add_argument(directory)
                options.add_argument(profile)
                self.driver = webdriver.Chrome(options=options)

    def setSubDriver(self):
        self.grabber.driver = self.driver
