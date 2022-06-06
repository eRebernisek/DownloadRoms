import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import xlsxwriter


# Configura o Selenium no ambiente Linux para utilizar o Firefox
firefox = webdriver.Firefox(executable_path='./geckodriver')
sitePage = 0


def openBrowser():
    global urlJogo
    for i in range(1, 3):
        sitePage = i
        url = 'https://romsplanet.com/roms/gameboy-advance?page='+str(sitePage)
        print(url)
        firefox.get(url)
        time.sleep(1)
        readValues()
        print('--------------------------------------------------------------')


def openTest():
    global urlJogo
    sitePage = 1
    url = 'https://romsplanet.com/roms/gameboy-advance?page='+str(sitePage)
    firefox.get(url)
    time.sleep(1)
    readValues()
    print('--------------------------------------------------------------')


def readValues():
    global urlJogo
    global firefox
    itemList = firefox.find_elements_by_css_selector('a.flag')
    for item in itemList:
        linkJogo = item.get_attribute('href')

        firefox.execute_script("window.open('"+str(linkJogo)+"');")
        time.sleep(1)
        

        firefox.switch_to.window(firefox.window_handles[1])
        firefox.close()


if __name__ == '__main__':
    os.system('clear')
    openBrowser()
    # openTest()
    firefox.close()
