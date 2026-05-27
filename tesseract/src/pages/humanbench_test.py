import pytesseract, time, pyautogui, os, re

from playwright.sync_api import sync_playwright
from PIL import Image

class HumanBenchTest:
    def __init__(self, page):
        self.page = page
        self.reaction_time_locator = page.locator(".reactiontime h3")
        self.path = "assets/imgs/"
        self.lista_resultados = []
        self.escala_tela = 1.75

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def open_browser(self):
        print("Carregando página ... ")
        self.page.goto("https://humanbenchmark.com/tests/reactiontime")
        time.sleep(3)
        pyautogui.hotkey('win', 'up')
        time.sleep(1)
    
    def clicar_reaction_time_test(self):
        time.sleep(2)
        while True:
            try:
                img_reaction = pyautogui.locateOnScreen('assets/reaction_test.png', confidence=0.8)
                pyautogui.click(img_reaction, duration=1)

                if img_reaction:
                    pyautogui.click(img_reaction)
                print(f'O elemento {img_reaction} foi encontrado e clicado!')
                break
            except Exception:
                print(f'Elemento {img_reaction} não foi encontrado')            

            time.sleep(2)

    def process_screenshot(self, tentativa):
        x = int(1200 * self.escala_tela)
        y = int(390 * self.escala_tela)
        w = int(500 * self.escala_tela)
        h = int(129 * self.escala_tela)

        regiao_captura = (x, y, w, h)

        img_save = pyautogui.screenshot(region=regiao_captura)
        nome_arquivo = f"{self.path} screen_{tentativa}.png"
        img_save.save(nome_arquivo)

        try:
            click_ms = pytesseract.image_to_string(img_save, lang="eng", config="--psm 6")
            texto_limpo = click_ms.strip().replace("\n", "")
            apenas_numeros = re.findall(r'\d+', texto_limpo)
            
            resultado_final = (f"{apenas_numeros[0]} ms" if apenas_numeros else texto_limpo)
            self.lista_resultados.append(f"Tentativa {tentativa}: {resultado_final}")
            
        except Exception as e:
            self.lista_resultados.append(f"Tentativa {tentativa}: Erro OCR ({e})")

    def clicar_wait_estart(self):
        time.sleep(2)

        for tentativa in range(1,6):
            print(f"\n --- Iniciando {tentativa} ---- ")
            while True:
                try:
                    img_click = pyautogui.locateOnScreen('assets/click.png', confidence=0.8)
                    if img_click:
                        pyautogui.click(img_click)
                        print(f'O elemento {img_click} foi encontrado e clicado!')

                        break
                except:
                    pass

            time.sleep(0.5)
            self.process_screenshot(tentativa)

            if tentativa < 5:
                print("Avançando para a próxima rodada...")
                pyautogui.click(960, 540)
                time.sleep(1.5)

        print(" -------- Informações das extrações ---------- ")
        for resultado in self.lista_resultados:
            print(resultado)

