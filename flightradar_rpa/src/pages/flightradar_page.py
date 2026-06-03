import pyautogui, time, random

class FlightRadarPage:

    def __init__(self, page):
        self.page = page
        self.url = "https://www.flightradar24.com/"
        self.txt_codigo_aviao = page.locator("div.data-row .aircraft-type-code, h2[data-test='aircraft-registration']").first
        self.txt_origem = page.locator("div[data-test='flight-origin-name']").first
        self.txt_destino = page.locator("div[data-test='flight-destination-name']").first
    
    def iniciar_navegador(self):
        self.page.goto(self.url, timeout=100000)
        self.page.get_by_role("button", name="Agree and close").click()
        self.page.get_by_role("button", name="Close").click()

        time.sleep(1)
        pyautogui.hotkey('win', 'up')
        time.sleep(2)

        print("Site aberto e poups fechadas!")
    
    def simular_movimento_mapa(self):
        print("Simulando exploração do usuário movendo o mouse pelo mapa...")
        largura, altura = pyautogui.size()
        centro_x, centro_y = largura // 2, altura // 2
        
        for _ in range(3):
            offset_x = random.randint(-150, 150)
            offset_y = random.randint(-150, 150)

            pyautogui.moveTo(centro_x + offset_x, centro_y + offset_y, duration=0.8)
            time.sleep(0.5)

    def selecionar_e_extrair_aeronave(self):
        print("Iniciando busca visual por aeronaves na tela...")
        caminho_asset = "assets/aviao1.png" 
        
        for tentativa in range(1, 11):
            try:
                coordenada = pyautogui.locateCenterOnScreen(caminho_asset, confidence=0.7)
                
                if coordenada:
                    print(f"Avião localizado na coordenada: {coordenada}! Efetuando clique...")
                    pyautogui.click(coordenada, duration=0.5)
                    time.sleep(2)
                    
                    self._coletar_dados_painel()
                    return True
            except Exception:
                pass
            time.sleep(1)
            
        print("Não foi possível avistar nenhuma aeronave correspondente ao print nesta execução.")
        return False
    
    def _coletar_dados_painel(self):
        print("Extraindo informações textuais do painel lateral...")
        
        try:
            self.txt_codigo_aviao.wait_for(state="visible", timeout=8000)
            
            codigo = self.txt_codigo_aviao.inner_text().strip()
            origem = self.txt_origem.inner_text().strip() if self.txt_origem.count() > 0 else "Não informada"
            destino = self.txt_destino.inner_text().strip() if self.txt_destino.count() > 0 else "Não informada"
            
            print("\n === DADOS DA AERONAVE SELECIONADA ===")
            print(f"Identificação/Código: {codigo}")
            print(f"Origem: {origem}")
            print(f"Destino: {destino}")
            print("=========================================\n")
            
        except Exception as e:
            print(f"Erro ao tentar mapear propriedades do painel: {e}")
        
