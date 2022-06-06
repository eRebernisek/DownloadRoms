import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
# import xlsxwriter

# Configura o Selenium no ambiente Linux para utilizar o Firefox
firefox = webdriver.Firefox(executable_path='./geckodriver')
sitePage = 0
nomeJogo = ""
jogosComErro = []


def openBrowser():
    global urlJogo
    global sitePage
    global jogosComErro
    # Ajustar de acordo com número de páginas do site
    for i in range(15, 51):
        print('---------------Salvando página '+str(i)+'---------------')
        sitePage = i
        url = 'https://romsplanet.com/roms/gameboy-advance?page='+str(sitePage)

        firefox.switch_to.window(firefox.window_handles[0])

        firefox.get(url)
        time.sleep(1)

        listaJogos()

        print('------------Página '+str(i)+' salva com sucesso---------------')
        print('------------------------------------------------------------')


def listaJogos():
    global firefox

    itemList = firefox.find_elements_by_css_selector('a.flag')

    salvaJogo(itemList)
    # salvaTest(itemList)


def salvaJogo(itemList):
    global urlJogo
    global firefox
    global nomeJogo

    for item in itemList:
        print('----------Salvando '+str(item.text)+'----------')
        linkJogo = item.get_attribute('href')

        # Abre link do jogo em nova aba
        firefox.execute_script("window.open('"+str(linkJogo)+"');")
        firefox.switch_to.window(firefox.window_handles[1])

        # verifica se a pagina carregou as img
        imgLen = 0
        btnLen = 0

        timer = time.time()
        startTime = timer
        thisTime = 0

        while not(imgLen > 1 and btnLen > 0):
            imageList = firefox.find_elements_by_tag_name('img')
            tempBtn = firefox.find_elements_by_css_selector('a.btn__download')
            btnLen = len(tempBtn)
            imgLen = len(imageList)
            thisTime = round((time.time() - startTime), 2)

            if thisTime > 3:
                startTime = timer.time()
                firefox.refresh()

        imgLogo = imageList[1]
        btnDownload = tempBtn[0]

        # salva imagem do jogo
        print('---------------Salvando imagem---------------')
        imgUrl = str(imgLogo.get_attribute('src'))
        imgTitle = str(imgLogo.get_attribute('title'))
        imgTitle = imgTitle.replace(" ", "_")
        imgTitle = imgTitle.replace("(", "")
        imgTitle = imgTitle.replace(")", "")
        imgTitle = imgTitle.replace("&", "and")

        print('Nome do jogo: '+imgTitle)
        cmdImg = 'wget '+imgUrl+' -O images/gba/'+imgTitle+'.png'

        # faz downlod do jogo
        print('---------------Salvando Jogos---------------')
        print('Imagens: '+str(imgLen))
        print('Links: '+str(btnLen))
        btnDownload.click()
        print('-----Redirecionado para download-----')

        # verifica se o link da pagina carregou
        timer = time.time()
        startTime = timer
        thisTime = 0
        linkLen = 0
        canRedirect = True
        while linkLen < 1:
            link = firefox.find_elements_by_link_text('click here')
            linkLen = len(link)

            thisTime = round((time.time() - startTime), 2)

            if thisTime > 3 and canRedirect:
                print('-----Erro para download-----')
                btnDownload.click()
                canRedirect = False

            if thisTime > 10:
                startTime = timer.time()
                firefox.refresh()

        print('-----Achado url download-----')
        urlDownload = link[0].get_attribute('href')
        # Sai da tela antes que faça download manual
        firefox.close()
        firefox.switch_to.window(firefox.window_handles[0])

        cmdJogo = 'wget ' + urlDownload
        cmdJogo = cmdJogo + ' -O roms/gba/'+imgTitle+'.zip --no-check-certificate'
        os.system(cmdImg)
        os.system(cmdJogo)
        print('---------------Jogo salvo com sucesso---------------')


if __name__ == '__main__':
    os.system('clear')
    openBrowser()
    # openTest()
    firefox.close()
