import time, random
import re
from playwright.sync_api import Page
import pyautogui

class BuscaPrecoPages:
    def __init__(self, page: Page, url: str):
        self.page = page
        self.url = url
        self.resultados_coleta = {}
    
    '''def espera_humana(self):
        espera_humana = random.uniform(3.5, 7.2)
        print(f" Pausa humanizada de {espera_humana:.2f} segundos...")
        time.sleep(espera_humana)'''

    def abrir_portal(self):
        print(f" Acessando o Busca Preço SEFAZ: {self.url}")
        self.page.goto(self.url, wait_until="domcontentloaded")
        self.page.bring_to_front()
        time.sleep(2)
        
        pyautogui.hotkey('win', 'up')
        time.sleep(1)

    def pesquisar_lista_itens(self, lista_itens):
        for item in lista_itens:
            print(f"  Recuperando dados para o item: {item}...")
            self.resultados_coleta[item] = []
            
            try:
                campo_busca = self.page.locator("input#descricaoProd")
                botao_pesquisar = self.page.locator("button[name='action']")
                
                campo_busca.fill(item)
                botao_pesquisar.click()
                
                print(" Aguardando renderização dos resultados...")
                self.page.wait_for_selector(".card.small.p.hoverable", state="visible", timeout=8000)
                
                cards = self.page.locator(".card.small.p.hoverable").all()
                vagas_analise = cards[:5]
                
                for card in vagas_analise:
                    try:
                        nome_produto = card.locator(".indigo span").first.inner_text(timeout=3000).strip()
                        texto_preco = card.locator("p:has-text('R$')").first.inner_text(timeout=3000)
                        preco_limpo = float(re.sub(r'[^\d,]', '', texto_preco).replace(',', '.'))
                        
                        paragrafos = card.locator(".card-content.principal p").all()
                        
                        if len(paragrafos) >= 3:
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
                time.sleep(1.5)
                
            except Exception as e:
                print(f"  Item '{item}' não gerou resultados ou excedeu tempo de resposta: {e}")
               
                self.page.goto(self.url, wait_until="domcontentloaded")
                time.sleep(1.5)
                
        return self.resultados_coleta

