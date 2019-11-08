from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
import time
import PIL.Image, io, base64

class connection:

    #TODO replace with CSD file for all config insted of seperate files to make more orginized
    def __helper_load_config(self,name):
        #loads file and returns a list but if the file dose not exist it returns None
        try:
            FP = open(name,'r')
            rawString = FP.read()
            listed = rawString.split("\n")[:-1]
            return listed
        except:
            return None

    def __init__(self,health_fail = 0.0 , tool_fail = ['','','',''], ammo_fail = {'pass':False}, heal_fail = {'pass':False}, armour_fail = {'pass':False}, time_fail = 0, player_fail = 0):
        #define varables
        self.driver = None
        self.FAILED_HEALTH = health_fail
        self.FAILED_TOOLS = tool_fail
        self.FAILED_AMMO = ammo_fail
        self.DEFAULT_AMMO = {'pass':True}
        self.FAILED_HEALING = heal_fail
        self.DEFAULT_HEALING = {'pass':True}
        self.FAILED_ARMOUR = armour_fail
        self.FAILED_RED_TIME = time_fail
        self.FAILED_PLAYER_NUM = player_fail

    def set_driver(self,driver = 'firefox'):
        #loads the driver

        #firefox
        if driver == 'firefox':
            options = webdriver.FirefoxOptions()
            #disables webgl to allow grabing of the screen
            options.set_preference("webgl.disabled",True)
            config = self.__helper_load_config("firefox_profile")
            if config == None:
                self.driver = webdriver.Firefox(options=options)
            else:
                profile = webdriver.FirefoxProfile(config[0])
                self.driver = webdriver.Firefox(firefox_profile=profile, options=options)

        if driver == 'chrome':
            config = self.__helper_load_config("chrome_profile")
            options = webdriver.ChromeOptions()
            #disables webgl to allow grabing of the screen
            options.add_argument("--disable-webgl ")

            if config == None:
                self.driver = webdriver.Chrome(options=options)
            else:
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

    def __get_armour(self):
        equipedArmor = {'pass':True}
        equipment = self.driver.find_elements_by_class_name('ui-armor-counter')
        for equiped in equipment:
            Eid = equiped.get_attribute("id")
            subElement = equiped.find_elements_by_class_name("ui-armor-level")
            if len(subElement) < 1:
                continue
            name = Eid.split("-")[2]
            equipedArmor.update({name:str(subElement[0].text)})

        return equipedArmor

    def __get_image_canvas(self):
        #for this to work webgl has to be disabled

        #retrives canvas
        canvas = self.driver.find_element_by_id("cvs")

        #retrives base64 text of image
        base64Text = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

        #decodes and sets up bytes object
        png_RB = base64.b64decode(base64Text)
        FP = io.BytesIO(png_RB)

        #reads and returns image object
        image = PIL.Image.open(FP)
        return image

    def __get_red_time(self):

        #gets element
        timeEle = self.driver.find_element_by_id("ui-gas-timer")

        stringValue = timeEle.text

        #convert string
        min, sec = stringValue.split(":")

        min = int(min)
        sec = int(sec)

        #convert min to seconds and add them
        totalSec = (min * 60) + sec

        return totalSec

    def __get_players_left(self):

        #gets element

        counterEle = self.driver.find_element_by_id("ui-map-counter-default")

        stringValue = counterEle.text

        intVal = int(stringValue)

        return intVal

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

    def get_armour(self):
        try:
            return self.__get_armour()
        except:
            return self.FAILED_ARMOUR

    def get_red_time(self):
        try:
            return self.__get_red_time()
        except:
            return self.FAILED_RED_TIME

    def get_players_left(self):
        try:
            return self.__get_players_left()
        except:
            return self.FAILED_PLAYER_NUM

    def get_image(self):
        #TODO add later webgl image grabing
        return self.__get_image_canvas()

if __name__ == '__main__':
    a = connection()
    a.FAILED_HEALTH = 100.0
    a.set_driver(driver='firefox')
    a.load_page()
    a.login("bot")
    data = None
    run = True
    time.sleep(10)
    a.get_image().show()
    while run:
        ndata = {'health':a.get_health(),"tool":a.get_tools(),'ammo':a.get_ammo(),'healing':a.get_healing(),'armor':a.get_armour(),'players':a.get_players_left()}
        if ndata != data:
            data = ndata
            print(data)

        if data["health"] <= 0.0:
            if input("contine?[y/n]:") == "y":
                continue
            a.get_image().show()
            print(a.get_red_time())
            a.close()
            run = False
