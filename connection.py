from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
import time

class connection:

    def __helper_load_config(self,name):
        #loads file and returns a list but if the file soe not exist it returns None
        try:
            fp = open(name,'r')
            rd = fp.read()
            d = rd.split("\n")[:-1]
            return d
        except:
            return None

    def __init__(self,health_fail = 0.0 , tool_fail = ['','','',''], ammo_fail = {'pass':False}):
        #define varables
        self.driver = None
        self.FAILED_HEALTH = health_fail
        self.FAILED_TOOLS = tool_fail
        self.FAILED_AMMO = ammo_fail
        self.DEFALT_AMMO = {'pass':True}

    def set_driver(self,driver = 'firefox'):
        #loads the driver        

        #firefox
        if driver == 'firefox':
            config = self.__helper_load_config("firefox_profile")
            if config == None:
                self.driver = webdriver.Firefox()
            else:
                profile = webdriver.FirefoxProfile(config[0])
                self.driver = webdriver.Firefox(profile)


    def close(self):
        self.driver.close()

    def load_page(self):
        #opens webpage

        self.driver.get("http://surviv.io")

    def login(self,name):
        #logs in/joins the game
        
        #finds the join buttons
        join_solo = self.driver.find_element_by_id("btn-start-mode-0")

        #finds name input
        name_input = self.driver.find_element_by_id('player-name-input-solo')

        #clears the input
        name_input.clear()

        #inputs the name
        name_input.send_keys(name)

        #clicks join game
        join_solo.click()

    def __get_health(self):
        #gets health of player

        health_bar = self.driver.find_element_by_id("ui-health-actual")
        health_str = health_bar.get_property('attributes')['2']['value'].split(';')[1].split(":")[1]
        health_float = float(health_str[:-1])
        return health_float

    def __get_tools(self):
        #gets equipt tools
        
        tools = self.driver.find_elements_by_class_name("ui-weapon-name")
        
        toolList = []

        for tool in tools:
            toolList += [tool.text]

        return toolList

    def __get_ammo(self):
        #gets ammo listing

        ammoList = self.driver.find_element_by_id("ui-ammo-interactive").find_elements_by_css_selector("*")
        ammoDic = self.DEFALT_AMMO

        for ammo in ammoList:
            if ammo.get_attribute("id") == "":
                continue

            ammoName = str(ammo.get_attribute("id").split("-")[2])
            ammoData = str(ammo.find_element_by_class_name("ui-loot-count").text)

            ammoDic.update({ammoName:ammoData})

        return ammoDic


    def __get_healing(self):
        None

    def get_health(self):
        try:
            return self.__get_health()
        except:
            return self.FAILED_HEALTH

    def get_tools(self):
        try:
            return self.__get_tools()
        except:
            return self.FAILED_TOOLS

    def get_ammo(self):
        try:
            return self.__get_ammo()
        except:
            return self.FAILED_AMMO

if __name__ == '__main__':
    a = connection()
    a.set_driver()
    a.load_page()
    a.login("bot")
    time.sleep(20)
    data = None
    while True:
        ndata = {'health':a.get_health(),"tool":a.get_tools(),'ammo':a.get_ammo()}
        if ndata != data:
            data = ndata
            print(data)

        if data["health"] == 0.0:
            if input("contine?[y/n]:") == "y":
                continue
            a.close()



