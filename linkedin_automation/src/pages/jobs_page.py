import urllib.parse
from src.utils.config import Config

class LinkedinJobsPage:
    def __init__(self, page):
        self.page = page
        self.cards_vagas = page.locator(".jobs-search-results-list li.jobs-search-results__list-item")

    def buscar_vagas(self):
        termo_codificado = urllib.parse.quote(Config.TERMO_PESQUISA)
        url_busca = f"https://www.linkedin.com/jobs/search/?keywords={termo_codificado}"
        
        print(f" Buscando por: '{Config.TERMO_PESQUISA}'...")
        self.page.goto(url_busca)
        self.page.wait_for_load_state("networkidle")

    def coletar_tres_primeiras_vagas(self):
        lista_vagas = []
        
        self.cards_vagas.first.wait_for(state="visible", timeout=15000)
        limite = min(3, self.cards_vagas.count())
        print(f" Extraindo dados das {limite} primeiras vagas encontradas...")

        for i in range(limite):
            card = self.cards_vagas.nth(i)
            card.scroll_into_view_if_needed()
            
            titulo_el = card.locator(".job-card-list__title")
            empresa_el = card.locator(".job-card-container__primary-description")
            
            titulo = titulo_el.inner_text().strip() if titulo_el.count() > 0 else "Título Indisponível"
            empresa = empresa_el.inner_text().strip() if empresa_el.count() > 0 else "Empresa Indisponível"
            
            lista_vagas.append({
                "posicao": i + 1,
                "titulo": titulo,
                "empresa": empresa
            })
            
        return lista_vagas
