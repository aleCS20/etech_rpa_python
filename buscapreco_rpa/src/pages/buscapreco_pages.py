import time, random
import re
from playwright.sync_api import Page
import pyautogui

class BuscaPrecoPages:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url
        self.resultados_coleta = {}
    
    def _espera_humana(self, min_segundos=2.5, max_segundos=5.5):
        tempo_espera = random.uniform(min_segundos, max_segundos)
        print(f" Pausa estratégica de {tempo_espera:.2f}s...")
        time.sleep(tempo_espera)

    def abrir_portal(self):
        print(f" Acessando o Busca Preço SEFAZ: {self.url}")
        self.page.goto(self.url, wait_until="domcontentloaded")
        self.page.bring_to_front()
        time.sleep(2)
        
        pyautogui.hotkey('win', 'up')
        time.sleep(1)

    def pesquisar_lista_itens(self, lista_itens):
        for item in lista_itens:
            print(f"\n Minerando dados para o item: {item}...")
            self.resultados_coleta[item] = []
            
            try:
                campo_busca = self.page.locator("input#descricaoProd")
                botao_pesquisar = self.page.locator("button[name='action']")
                
                campo_busca.click()
                campo_busca.clear()
                self._espera_humana(0.5, 1.2)
                
                print(f" Digitando sequencialmente: '{item}'...")
                campo_busca.press_sequentially(item, delay=180)
                
                self._espera_humana(1.5, 2.8) 
                botao_pesquisar.click()
                
                print(" Aguardando processamento e retorno dos cards da SEFAZ...")
                self._espera_humana(5.0, 8.5)
                
                self.page.wait_for_selector(".card.small.p.hoverable", state="visible", timeout=10000)
                
                cards = self.page.locator(".card.small.p.hoverable").all()
                vagas_analise = cards[:5] 
                
                for card in vagas_analise:
                    try:
                        nome_produto = card.locator(".indigo span").first.inner_text(timeout=3000).strip()
                        
                        texto_preco = card.locator("p:has-text('R$')").first.inner_text(timeout=3000)
                        preco_limpo = float(re.sub(r'[^\d,]', '', texto_preco).replace(',', '.'))
                        
                        paragrafos = card.locator(".card-content.principal p").all()
                        
                        if (len(paragrafos) >= 3):
                            estabelecimento = paragrafos[2].inner_text(timeout=3000).strip()
                        else:
                            estabelecimento = paragrafos[-1].inner_text(timeout=3000).strip()
                        
                        oferta_real = {
                            "nome_produto_sefaz": nome_produto,
                            "estabelecimento": estabelecimento if estabelecimento else "Não Informado",
                            "preco": preco_limpo
                        }
                        
                        self.resultados_coleta[item].append(oferta_real)
                        
                    except Exception as erro_sub_card:
                        print(f"  Ignorando inconsistência de leitura no card: {erro_sub_card}")
                        
                print(f" Processadas {len(self.resultados_coleta[item])} ofertas reais para: {item}")
                
                self.page.goto(self.url, wait_until="domcontentloaded")
                
                print("  Descanso preventivo de sessão para evitar bloqueio anti-bot...")
                self._espera_humana(4.0, 7.5)
                
            except Exception as e:
                print(f" Item '{item}' não retornou dados ou caiu na barreira do site: {e}")
                self.page.goto(self.url, wait_until="domcontentloaded")
                self._espera_humana(6.0, 10.0)
                
        return self.resultados_coleta

