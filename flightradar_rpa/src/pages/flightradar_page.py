import pyautogui
import time
import random

class FlightRadarPage:
    def __init__(self, page):
        self.page = page
        self.url = "https://www.flightradar24.com/"
        
        self.assets_avioes = [
            "assets/aviao1.png",
            "assets/aviao2.png",
            "assets/aviao3.png",
            "assets/aviao4.png",
            "assets/aviao5.png",
            "assets/aviao6.png"
        ]
        
        # Lista para armazenar as coordenadas lidas e evitar clicar no mesmo avião repetidamente
        self.avioes_clicados = []
        
        self.txt_codigo_aviao = page.locator("h2[data-test='aircraft-registration'], .aircraft-type-code").first
        self.txt_origem = page.locator("div[data-test='flight-origin-name']").first
        self.txt_destino = page.locator("div[data-test='flight-destination-name']").first

    def iniciar_navegador(self):
        print("🌐 Carregando FlightRadar24...")
        self.page.goto(self.url, timeout=100000, wait_until="commit")
        
        self.page.bring_to_front()
        time.sleep(1)
        pyautogui.hotkey('win', 'up')
        time.sleep(2)

        try:
            self.page.get_by_role("button", name="Agree and close").click(timeout=8000)
        except: pass
        
        try:
            self.page.get_by_role("button", name="Close").click(timeout=5000)
        except: pass
        print("✅ Pop-ups iniciais tratadas.")
        
        time.sleep(3)

        print("🧹 Injetando super script de limpeza de interface...")
        try:
            # CORREÇÃO DO SYNTAX ERROR: Removido o caractere '#' inadequado do bloco JS
            self.page.evaluate("""
                const seletores = [
                    '.commercial-sidebar', 
                    '.sidebar-unauthenticated', 
                    '#sidebar-unauthenticated',
                    'aside[class*="sidebar"]',
                    'div[class*="sidebar-premium"]',
                    '.sticky-sidebar'
                ];
                
                seletores.forEach(seletor => {
                    const elementos = document.querySelectorAll(seletor);
                    elementos.forEach(el => {
                        el.remove();
                    });
                });

                const mapContainer = document.querySelector('#map-container, .map-container');
                if (mapContainer) {
                    mapContainer.style.width = '100%';
                }
            """)
            
            self.page.evaluate("window.dispatchEvent(new Event('resize'));")
            print("🚀 Evento de Resize disparado no mapa!")
        except Exception as e:
            print(f"⚠️ Erro ao tentar injetar destruição de elemento: {e}")

        print("🔍 Aplicando ajuste de escala de layout...")
        self.page.evaluate("document.body.style.zoom = '0.85'")
        time.sleep(2)

    def simular_movimento_mapa(self):
        print("🖱️ Simulando exploração do usuário movendo o mouse pelo mapa...")
        largura, altura = pyautogui.size()
        centro_x, centro_y = largura // 2, altura // 2
        
        for _ in range(3):
            offset_x = random.randint(-100, 100)
            offset_y = random.randint(-100, 100)
            pyautogui.moveTo(centro_x + offset_x, centro_y + offset_y, duration=0.6)
            time.sleep(0.4)

    def selecionar_e_extrair_aeronave(self):
        print("🎯 Iniciando busca visual multimagem por aeronaves na tela...")
        url_original = self.page.url
        
        for tentativa in range(1, 6):
            print(f"🔄 Varredura de tela - Tentativa {tentativa}/5...")
            
            for caminho_img in self.assets_avioes:
                try:
                    coordenada = pyautogui.locateCenterOnScreen(caminho_img, confidence=0.55)
                    
                    if coordenada:
                        # Convertendo numpy.int64 para int nativo do Python para evitar problemas de tipo
                        x, y = int(coordenada[0]), int(coordenada[1])
                        
                        # FILTRO DE REPETIÇÃO: Verifica se já não clicamos muito perto dessa coordenada antes
                        if any(abs(x - cx) < 15 and abs(y - cy) < 15 for cx, cy in self.avioes_clicados):
                            continue # Ignora e pula para o próximo para não repetir o mesmo avião
                        
                        print(f"✈️ Avião avistado pelo print '{caminho_img}' em ({x}, {y})")
                        
                        # Move de forma visível até o alvo
                        pyautogui.moveTo(x, y, duration=0.5)
                        
                        # CORREÇÃO DE CLIQUE NO CANVAS: O clique instantâneo falha no WebGL.
                        # UsamosmouseDown e mouseUp com um intervalo (clique humano e firme)
                        pyautogui.mouseDown(x, y)
                        time.sleep(0.2)
                        pyautogui.mouseUp(x, y)
                        
                        time.sleep(4) # Janela de tempo para o servidor carregar a rota
                        
                        # Auditoria por modificação de URL
                        url_pos_clique = self.page.url
                        if url_original != url_pos_clique:
                            print(f"🎯 [SUCESSO DE CLIQUE] Aeronave selecionada! URL: {url_pos_clique}")
                            self.avioes_clicados.append((x, y)) # Registra na lista de exclusão
                            
                            self._coletar_dados_painel()
                            return True
                        else:
                            print("⚠️ O mouse clicou, mas o Canvas não registrou o foco. Tentando próximo...")
                            
                except Exception:
                    pass
                    
            time.sleep(1.5)
            
        print("❌ Fim das tentativas. Nenhum avião foi selecionado de verdade.")
        return False

    def _coletar_dados_painel(self):
        print("📥 Analisando painel de informações...")
        try:
            self.txt_codigo_aviao.wait_for(state="visible", timeout=6000)
            
            codigo = self.txt_codigo_aviao.inner_text().strip()
            origem = self.txt_origem.inner_text().strip() if self.txt_origem.count() > 0 else "Não informada"
            destino = self.txt_destino.inner_text().strip() if self.txt_destino.count() > 0 else "Não informada"
            
            print("\n📊 === DADOS DA AERONAVE CAPTURADA ===")
            print(f"🔹 Matrícula/Código: {codigo}")
            print(f"📍 Origem: {origem}")
            print(f"🏁 Destino: {destino}")
            print("=========================================\n")
        except Exception:
            print("⚠️ A URL mudou confirmando o clique, mas o painel esquerdo continua oculto pelo CSS responsivo.")
            