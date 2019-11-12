from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver import ActionChains

class interacter:

    def __init__(self):
        pass
        self.driver = None

    def rightClick(self,element):

        actionChains = ActionChains(self.driver)

        actionChains.context_click(element).perform()


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

    def __setTool(self,slot):

        id = "ui-weapon-id-" + str(slot)

        element = self.driver.find_element_by_id(id)

        element.click()

        return 0

    def __useHealing(self,item):

        id = "ui-loot-" + str(item)

        element = self.driver.find_element_by_id(id)

        element.click()

        return 0

    def __dropTool(self,slot):

        id = "ui-weapon-id-" + str(slot)

        element = self.driver.find_element_by_id(id)

        self.rightClick(element)

        return 0

    def __dropLoot(self,item):

        id = "ui-loot-" + str(item)

        element = self.driver.find_element_by_id(id)

        self.rightClick(element)

        return 0

    def useHealing(self,item):
        try:
            return self.__useHealing(item)
        except:
            return -1

    def setTool(self,slot):
        try:
            return self.__setTool(slot)
        except:
            return -1

    def dropTool(self,slot):
        try:
            return self.__dropTool()
        except:
            return -1

    def dropLoot(self,slot):
        try:
            return self.__dropLoot(slot)
        except:
            return -1
