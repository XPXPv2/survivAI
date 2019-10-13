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

    def __init__(self,health_fail = 0.0 , tool_fail = ['','','',''], ammo_fail = {'pass':False}, heal_fail =  {'pass':False}):
        #define varables
        self.driver = None
        self.FAILED_HEALTH = health_fail
        self.FAILED_TOOLS = tool_fail
        self.FAILED_AMMO = ammo_fail
        self.DEFAULT_AMMO = {'pass':True}
        self.FAILED_HEALING = heal_fail
        self.DEFAULT_HEALING = {'pass':True}

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

        if driver == 'chrome':
            config = self.__helper_load_config("chrome_profile")
            if config == None:
                self.driver = webdriver.Chrome()
            else:
                options = webdriver.ChromeOptions()
                directory = 'user-data-dir=' + config[0]
                profile = 'profile-directory=' + config[1]
                options.add_argument(directory)
                options.add_argument(profile)
                self.driver = webdriver.Chrome(options=options)


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

        ammoList = self.driver.find_element_by_id("ui-ammo-interactive")
        ammoList = ammoList.find_elements_by_css_selector("*")
        ammoDic = self.DEFAULT_AMMO

        for ammo in ammoList:
            if ammo.get_attribute("id") == "":
                continue

            ammoName = str(ammo.get_attribute("id").split("-")[2])
            ammoData = str(ammo.find_element_by_class_name("ui-loot-count").text)

            ammoDic.update({ammoName:ammoData})

        return ammoDic


    def __get_healing(self):
        #gets medic listing

        medicList = self.driver.find_element_by_id("ui-medical-interactive")
        medicList = medicList.find_elements_by_css_selector("*")
        medicDic = self.DEFAULT_HEALING

        for medic in medicList:
            if medic.get_attribute("id") == "":
                continue

            medicName = str(medic.get_attribute("id").split("-")[2])
            medicData = str(medic.find_element_by_class_name("ui-loot-count").text)

            medicDic.update({medicName:medicData})

        return medicDic

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

    def get_healing(self):
        try:
            return self.__get_healing()
        except:
            return self.FAILED_HEALING

if __name__ == '__main__':
    a = connection()
    a.FAILED_HEALTH = 100.0
    a.set_driver(driver='chrome')
    a.load_page()
    a.login("bot")
    data = None
    run = True
    while run:
        ndata = {'health':a.get_health(),"tool":a.get_tools(),'ammo':a.get_ammo(),'healing':a.get_healing()}
        if ndata != data:
            data = ndata
            print(data)

        if data["health"] == 0.0:
            if input("contine?[y/n]:") == "y":
                continue
            a.close()
            run = False
