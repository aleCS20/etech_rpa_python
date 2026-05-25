import re, time
import pyautogui

from playwright.sync_api import Page, expect

class RoboAiminig:
    def __init__(self, page):
        self.page = page

    def abrir_navegador_site(self):
        self.page.goto("https://aiming.pro/app#/play/tutorial/benchmark")
        time.sleep(2)
        #pyautogui.hotkey('win', 'up')
    
    def start_game(self):
        time.sleep(3)
        try:
            imagem = pyautogui.locateOnScreen('assets/play1.png', confidence=0.7)

            if (imagem is not None):
                #centro = pyautogui.center(imagem)
                pyautogui.click(imagem.x, imagem.y)
                print("Botão Play clicado - carregando tela do jogo ... ")
            else:
                print("Botão não encontrado na tela")

            time.sleep(3)
        
        except pyautogui.ImageNotFoundException:
            print("O botão 'play' não foi encontrado na tela")

    
    def fire_ball(self):
        largura, altura = pyautogui.size()
        centro_x = largura / 2
        centro_y = altura / 2
        print(centro_x, centro_y)

        pyautogui.click(centro_x, centro_y)

        time.sleep(3)

        cont = 59
        while (cont < 59):
            try:
                imagem = pyautogui.locateOnScreen('assets/ball1.png', confidence=0.6)
                pyautogui.click(imagem, duration=1)
            except:
                print("jogo não carregado!!")
            cont = cont - 1

        time.sleep(3)
    
    def finalizar_jogo(self):
        time.sleep(2)
        imagem = pyautogui.locateOnScreen('assets/exit.png', confidence=0.8)
        pyautogui.click(imagem)
    

