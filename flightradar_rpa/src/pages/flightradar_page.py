import cv2
import numpy as np
import pyautogui
import time
import random

from pathlib import Path

class FlightRadarPage:
    def __init__(self, page):
        self.page = page
        self.url = "https://www.flightradar24.com/"
        
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.templates_avioes = [
            self.base_dir / "assets" / "aviao1.png",
            self.base_dir / "assets" / "aviao2.png",
            self.base_dir / "assets" / "aviao3.png",
            self.base_dir / "assets" / "aviao4.png",
            self.base_dir / "assets" / "aviao5.png",
            self.base_dir / "assets" / "aviao6.png",
        ]
        
        self.confidence_limiar = 0.65
        self.distancia_duplicados = 30
        self.avioes_clicados_sucesso = []

        self.txt_codigo_aviao = page.locator("h2[data-test='aircraft-registration'], .aircraft-type-code").first
        self.txt_origem = page.locator("div[data-test='flight-origin-name']").first
        self.txt_destino = page.locator("div[data-test='flight-destination-name']").first

    def iniciar_navegador(self):
        print(" Carregando FlightRadar24 via Playwright...")
        self.page.goto(self.url, timeout=100000, wait_until="commit")
        
        self.page.bring_to_front()
        time.sleep(1)
        pyautogui.hotkey('win', 'up')
        time.sleep(2)

        try: self.page.get_by_role("button", name="Agree and close").click(timeout=5000)
        except: pass
        try: self.page.get_by_role("button", name="Close").click(timeout=5000)
        except: pass
        
        try:
            self.page.evaluate("""
                const anuncios = document.querySelectorAll('.commercial-sidebar, .sidebar-unauthenticated, #sidebar-unauthenticated, aside[class*="sidebar"]');
                anuncios.forEach(el => el.remove());
                const mapa = document.querySelector('#map-container, .map-container');
                if (mapa) mapa.style.width = '100%';
            """)
            self.page.evaluate("window.dispatchEvent(new Event('resize'));")
        except:
            print(" Não foi possível limpar os elementos de anúncio.")

        self.page.evaluate("document.body.style.zoom = '0.85'")
        time.sleep(2)
        print(" Interface preparada e limpa!")

    def _capturar_matriz_tela(self):
        img = pyautogui.screenshot()
        img = np.array(img)
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    def _remover_duplicados(self, pontos):
        filtrados = []
        for x, y in pontos:
            repetido = False
            for fx, fy in filtrados:
                if abs(x - fx) < self.distancia_duplicados and abs(y - fy) < self.distancia_duplicados:
                    repetido = True
                    break
            if not repetido:
                filtrados.append((x, y))
        return filtrados

    def varrer_e_clicar_aviao(self):
        print(" Capturando tela e processando matriz OpenCV...")
        matriz_tela = self._capturar_matriz_tela()
        pontos_encontrados = []

        for caminho_template in self.templates_avioes:
            if not caminho_template.exists():
                continue
                
            template = cv2.imread(str(caminho_template), cv2.IMREAD_COLOR)
            if template is None:
                continue

            resultado = cv2.matchTemplate(matriz_tela, template, cv2.TM_CCOEFF_NORMED)
            localizacoes = np.where(resultado >= self.confidence_limiar)

            h, w = template.shape[:2]
            for x, y in zip(localizacoes[1], localizacoes[0]):
                centro_x = int(x + w // 2)
                centro_y = int(y + h // 2)
                pontos_encontrados.append((centro_x, centro_y))

        pontos_unicos = self._remover_duplicados(pontos_encontrados)
        print(f" Foram detectados {len(pontos_unicos)} aviões candidatos na tela.")

        for x, y in pontos_unicos:
            if any(abs(x - cx) < 30 and abs(y - cy) < 30 for cx, cy in self.avioes_clicados_sucesso):
                continue

            print(f" Movendo e efetuando clique persistente em: ({x}, {y})")
            pyautogui.moveTo(x, y, duration=0.4)
            
            pyautogui.mouseDown(x, y)
            time.sleep(0.15)
            pyautogui.mouseUp(x, y)
            
            print("Aguardando confirmação visual do painel lateral...")
            time.sleep(2.5) 
            try:
                if self.txt_codigo_aviao.is_visible():
                    print(f" [SUCESSO] Painel detectado visualmente para a coordenada ({x}, {y})!")
                    self.avioes_clicados_sucesso.append((x, y))
                    self._extrair_dados_painel()
                    return True
                else:
                    print(" O painel não abriu para esta coordenada. Tentando próximo ponto...")
            except Exception:
                print(" Falha ao checar o elemento do painel. Prosseguindo...")

        print(" Nenhum avião da varredura atual pôde ser selecionado.")
        return False

    def _extrair_dados_painel(self):
        print(" Raspando propriedades textuais do painel...")
        try:
            self.txt_codigo_aviao.wait_for(state="visible", timeout=5000)
            codigo = self.txt_codigo_aviao.inner_text().strip()
            origem = self.txt_origem.inner_text().strip() if self.txt_origem.count() > 0 else "Não informada"
            destino = self.txt_destino.inner_text().strip() if self.txt_destino.count() > 0 else "Não informada"
            
            print("\n === DADOS CAPTURADOS COM SUCESSO ===")
            print(f"Código: {codigo}")
            print(f"Origem: {origem}")
            print(f"Destino: {destino}")
            print("=========================================\n")
        except Exception as e:
            print(f" Painel não respondeu ou seletores mudaram: {e}")

