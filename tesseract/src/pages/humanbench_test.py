import pytesseract, time, pyautogui

from playwright.sync_api import sync_playwright
from PIL import Image

class HumanBenchTest:
    def __init__(self, page):
        self.page = page
        self.reaction_time_locator = page.locator(".reactiontime h3")

    def open_browser(self):
        print("Carregando página ... ")
        self.page.goto("https://humanbenchmark.com/tests/reactiontime")
        
        time.sleep(2)
    
    def clicar_reaction_time_test(self):
        time.sleep(2)

        while True:
            try:
                img_reaction = pyautogui.locateOnScreen('assets/reaction_test.png', confidence=0.8)
                pyautogui.mouseDown(img_reaction, duration=1)
                print(f'O elemento {img_reaction} foi encontrado e clicado!')
                break
            except:
                print(f'Elemento {img_reaction} não foi encontrado')             
                break

            time.sleep(2)

    def clicar_wait_estart(self):
        time.sleep(2)

        while True:
            try:
                img_wait = pyautogui.locateOnScreen('assets/wait.png', confidence=0.8)
                pyautogui.mouseDown(img_wait, duration=1)
                print(f'O elemento {img_wait} foi encontrado e clicado!')
                break
            except:
                print(f'Elemento{img_wait}  não foi encontrado')             
                break

            time.sleep(5)
    
    #def testando_cliques(self):


