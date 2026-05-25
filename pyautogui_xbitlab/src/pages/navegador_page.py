import time
from playwright.sync_api import sync_playwright

class NavegadorPage:
    def __init__(self):
        self.playwriht = None
        self.browser = None
        self.page = None
    
    def iniciar_jogo(self, url: str):
        print("Iniciando o navegador...")
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False, 
            args=["--start-maximized"]
        )
    
        context = self.browser.new_context(no_viewport=True)
        self.page = context.new_page()
        
        print(f"Acessando: {url}")
        self.page.goto(url)

        self.page.wait_for_load_state("networkidle")
        
        print("Aguardando 3 segundos para estabilização...")
        time.sleep(3)
    
    def fechar(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    