from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys


class connection:

    def __init__(self):
        #define varables
        self.driver = None

    def set_driver(self,driver = 'firefox'):
        #loads the driver        

        #firefox
        if driver == 'firefox':
            self.driver = webdriver.Firefox()

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




if __name__ == '__main__':
    a = connection()
    a.set_driver()
    a.load_page()
    a.login("bot")
