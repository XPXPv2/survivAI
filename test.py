#Note this is a test script and will be rewritten into a class to handle fetching info from the server
from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
import time


driver = webdriver.Firefox()
driver.get("http://surviv.io")
print("starting")

def gethealth():
    global driver
    counter = driver.find_element_by_id("ui-health-counter")
    container = driver.find_element_by_id("ui-health-container")
    healthbar = driver.find_element_by_id("ui-health-actual")
    health = healthbar.get_property('attributes')['2']['value'].split(';')[1].split(":")[1]
    health = float(health[:-1])
    return health
    
def joinGame(name):
    global driver
    button = driver.find_element_by_id("btn-start-mode-0")
    nameInput = driver.find_element_by_id('player-name-input-solo')
    nameInput.clear()
    nameInput.send_keys(name)
    button.click()
    
def getItems():
    global driver
    objs = driver.find_elements_by_class_name("ui-weapon-name")
    items = []
    for item in objs:
        items += [item.text]
    return items
    
def getAmmo():
    global driver
    ammodisplay = driver.find_element_by_id("ui-ammo-interactive")
    ammolist = ammodisplay.find_elements_by_css_selector("*")
    ammo = {}
    for obj in ammolist:
        if obj.get_attribute("id") == "":
            continue
        oid = str(obj.get_attribute("id").split("-")[2])
        data = obj.find_element_by_class_name("ui-loot-count").text
        ammo.update({oid:str(data)})
    
    return ammo

def getArmor():
    global driver
    
joinGame("bot")
time.sleep(10)
health = gethealth()
items = getItems()
ammo = getAmmo() 

while True:
    newhealth = gethealth()
    newitems = getItems()
    newammo = getAmmo()
    
    if newhealth != health:
        print("Health: " + str(health) + " -> " + str(newhealth))
        health = newhealth
    
    if newitems != items:
        for index in range(len(items)):
            if newitems[index] != items[index]:
                print("Item #" + str(index + 1) + " " + str(items[index]) + " -> " + str(newitems[index]))
                
        items = newitems
        
    if newammo != ammo:
        for key in ammo.keys():
            if ammo[key] != newammo[key]:
                print(str(key) + " : " + str(ammo[key]) + " -> " + str(newammo[key]))
        ammo = newammo
