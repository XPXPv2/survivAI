from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys


class connection:

    def helper_load_config(self,name):
        #loads file and returns a list but if the file soe not exist it returns None
        try:

            fp = open(name,'r')
            rd = fp.read()
            d = rd.split("\n")[:-1]
            return d

         except:
            return None

    def __init__(self):
        #define varables
        self.driver = None

    def set_driver(self,driver = 'firefox'):
        #loads the driver        

        #firefox
        if driver == 'firefox':
            config = self.helper_load_config("firefox_profile")
            if config == None:
                self.driver = webdriver.Firefox()
            else:
                profile = webdriver.FirefoxProfile(config)
                self.driver = webdriver.Firefox(profile)

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

    def get_health(self):
        #gets health of player

        health_bar = self.driver.find_element_by_id("ui-health-actual")
        health_str = get_property('attributes')['2']['value'].split(';')[1].split(":")[1]
        health_float = float(health_str[:-1])
        return health_float

    def get_weapons(self):
        None

    def get_ammo(self):
        None

    def get_healing(self):
        None


if __name__ == '__main__':
    a = connection()
    a.set_driver()
    a.load_page()
    a.login("bot")
    while true:
        print(a.get_health())
