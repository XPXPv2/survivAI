class connection:

    def __init__(self):
        None

    def import(self):
        #imports moduals
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys as keys

    def init(self,driver = 'firefox'):
        self.driver = None
    
        #firefox
        if driver == 'firefox':
            self.driver = webdriver.Firefox()


