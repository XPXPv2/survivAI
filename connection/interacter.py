from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys

#TODO inplment class to interact with game
class interacter:

    def __init__(self):
        pass
        self.driver = None

    def loadPage(self):
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
