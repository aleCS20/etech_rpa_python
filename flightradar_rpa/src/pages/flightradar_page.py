import cv2
import numpy as np
import pyautogui
import time
import os
import easyocr
from pathlib import Path

class FlightRadarPage:
    def __init__(self, page):
        self.page = page
        self.url = "https://www.flightradar24.com/"
        
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.diretorio_imagens = self.base_dir / "img"
        
        os.makedirs(str(self.diretorio_imagens), exist_ok=True)
        
        print(" Inicializando redes neurais do EasyOCR para auditoria de imagens...")
        self.ocr_reader = easyocr.Reader(["pt", "en"])

        self.templates_avioes = [
            self.base_dir / "assets" / "aviao1.png",
            self.base_dir / "assets" / "aviao2.png",
            self.base_dir / "assets" / "aviao3.png",
            self.base_dir / "assets" / "aviao4.png",
            self.base_dir / "assets" / "aviao5.png",
            self.base_dir / "assets" / "aviao6.png"
        ]
        
        self.confidence_limiar = 0.70
        self.distancia_duplicados = 35
        self.avioes_clicados_sucesso = []
        self.ultimo_codigo_capturado = ""

        self.txt_codigo_aviao = page.get_by_test_id("aircraft-panel__header__callsign")
        self.txt_origem = page.get_by_test_id("aircraft-panel__airport-departure-city")
        self.txt_destino = page.get_by_test_id("aircraft-panel__airport-arrival-city")
        self.img_aviao_painel = page.get_by_test_id("aircraft-panel__image__image__0")

    def iniciar_navegador(self):
        print(" Carregando FlightRadar24 via Playwright...")
        largura_real, altura_real = pyautogui.size()
        self.page.set_viewport_size({"width": largura_real, "height": altura_real})
        self.page.goto(self.url, timeout=100000, wait_until="commit")
        
        self.page.bring_to_front()
        time.sleep(1)
        pyautogui.hotkey('win', 'up')
        time.sleep(2)

        try: self.page.get_by_role("button", name="Agree and close").click(timeout=6000)
        except: pass
        try: self.page.get_by_role("button", name="Close").click(timeout=4000)
        except: pass
        
        print(" Removendo barreiras comerciais para liberar a barra esquerda...")
        try:
            self.page.evaluate("""
                const comerciais = document.querySelectorAll('.commercial-sidebar, .sidebar-unauthenticated, #sidebar-unauthenticated, aside[class*="sidebar"], div[class*="sidebar-premium"]');
                comerciais.forEach(el => el.remove());
                
                const mapa = document.querySelector('#map-container, .map-container');
                if (mapa) {
                    mapa.style.width = '100%';
                    mapa.style.position = 'absolute';
                    mapa.style.left = '0';
                }
            """)
            self.page.evaluate("window.dispatchEvent(new Event('resize'));")
            print(" Mapa redimensionado nativamente em escala 1:1!")
        except Exception as e:
            print(f" Falha na limpeza de estilo: {e}")
            
        time.sleep(2)

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

    def varrer_e_clicar_aviao(self, meta_requisito=5):
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

        total_capturado = 0

        for x, y in pontos_unicos:
            if total_capturado >= meta_requisito:
                print(f" Meta de {meta_requisito} aviões atingida com sucesso!")
                break

            if x < 450:
                continue

            if any(abs(x - cx) < 25 and abs(y - cy) < 25 for cx, cy in self.avioes_clicados_sucesso):
                continue

            print(f" Efetuando clique ultra calibrado em: ({x}, {y})")
            pyautogui.moveTo(x, y, duration=0.4)
            
            pyautogui.mouseDown(x, y)
            time.sleep(0.15)
            pyautogui.mouseUp(x, y)
            
            print(" Validando atualização do painel de dados por TestID...")
            time.sleep(3.5) 

            try:
                if self.txt_codigo_aviao.is_visible():
                    codigo_atual = self.txt_codigo_aviao.inner_text().strip()
                    
                    if codigo_atual != self.ultimo_codigo_capturado and codigo_atual != "N/A":
                        print(f" Painel detectado! Nova aeronave ativa: {codigo_atual}!")
                        self.avioes_clicados_sucesso.append((x, y))
                        self.ultimo_codigo_capturado = codigo_atual
                        self._processar_e_salvar_foto_ocr(codigo_atual)
                        self._extrair_dados_painel()
                        
                        total_capturado += 1
                        print(f" Progresso atual: {total_capturado} de {meta_requisito} aviões salvos.\n")
                        
                        print(" Fechando painel lateral esquerdo para liberar o mapa...")
                        btn_fechar_painel = self.page.locator("button[data-testid='aircraft-panel__close-button'], .aircraft-panel-close, button:has-text('✕')").first
                        if btn_fechar_painel.count() > 0:
                            btn_fechar_painel.click(timeout=3000)
                            time.sleep(1.5)
                        
                    else:
                        print(" O painel exibe um registro repetido ou código N/A inválido.")
                else:
                    print(" Painel não foi reconhecido pelo Playwright nesta coordenada.")
            except Exception as e:
                print(f" Erro ao checar o estado do painel por TestID: {e}")

        print(f" Fim da varredura de tela. Total de novos aviões processados nesta rodada: {total_capturado}")
        return total_capturado

    def _processar_e_salvar_foto_ocr(self, codigo_voo):
        caminho_salvamento = self.diretorio_imagens / f"{codigo_voo}.png"
        print(f" Capturando recorte gráfico da foto da aeronave...")
        
        try:
            if self.img_aviao_painel.is_visible():
                self.img_aviao_painel.screenshot(path=str(caminho_salvamento))
                print(f" Foto salva com sucesso em: /img/{codigo_voo}.png")
                
                img_cv = cv2.imread(str(caminho_salvamento))
                
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                
                resultado_ocr = self.ocr_reader.readtext(gray)
                
                print(" [EasyOCR Audit] Textos secundários identificados na foto:")
                textos_coletados = [item[1] for item in resultado_ocr if item[2] > 0.4]
                if textos_coletados:
                    print(f"   ↳ Coletas: {textos_coletados}")
                else:
                    print("   ↳ Nenhuma inscrição de texto evidente detectada sobre a imagem.")
            else:
                print(" Esta aeronave não possui foto de exibição cadastrada no servidor do site.")
        except Exception as e:
            print(f"⚠️ Falha na execução da sub-pipeline de salvamento/OCR: {e}")

    def _extrair_dados_painel(self):
        print(" Extraindo dados textuais do painel lateral...")
        try:
            self.txt_codigo_aviao.wait_for(state="visible", timeout=4000)
            codigo = self.txt_codigo_aviao.inner_text().strip()
            origem = self.txt_origem.inner_text().strip() if self.txt_origem.is_visible() else "N/A - Not Available"
            destino = self.txt_destino.inner_text().strip() if self.txt_destino.is_visible() else "N/A - Not Available"
            
            print("\n =========================================")
            print("       DADOS DA AERONAVE CAPTURADA (RPA)    ")
            print("=========================================")
            print(f"  Identificação/Voo: {codigo}")
            print(f"  Cidade de Origem:  {origem}")
            print(f"  Cidade de Destino: {destino}")
            print("=========================================\n")
        except Exception as e:
            print(f" Erro ao capturar texto dos elementos: {e}")
