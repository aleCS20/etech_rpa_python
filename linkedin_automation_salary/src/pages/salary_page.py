import urllib.parse

class LinkedinSalaryPage:
    def __init__(self, page):
        self.page = page
        self.cards_vagas = page.locator(".jobs-search-results-list li.jobs-search-results__list-item")

    def pesquisar_vagas_internacionais(self, cargo, pais):
        cargo_encoded = urllib.parse.quote(cargo)
        pais_encoded = urllib.parse.quote(pais)
        
        url_busca = f"https://www.linkedin.com/jobs/search/?keywords={cargo_encoded}&location={pais_encoded}"
        
        print(f"Direcionando busca para o mercado de: {pais}...")
        self.page.goto(url_busca)
        self.page.wait_for_load_state("networkidle")

    def extrair_estimativas_salariais(self):       
        self.cards_vagas.first.wait_for(state="visible", timeout=15000)
        limite = min(5, self.cards_vagas.count())
        
        resultados = []
        print(f"Analisando os {limite} primeiros resultados em busca de dados financeiros...")

        for i in range(limite):
            card = self.cards_vagas.nth(i)
            card.scroll_into_view_if_needed()
            
            titulo_el = card.locator(".job-card-list__title")
            empresa_el = card.locator(".job-card-container__primary-description")
            
            salario_el = card.locator(".job-card-container__metadata-item--salary, .job-card-list__footer-item").first
            
            titulo = titulo_el.inner_text().strip() if titulo_el.count() > 0 else "N/A"
            empresa = empresa_el.inner_text().strip() if empresa_el.count() > 0 else "N/A"
            
            salario = salario_el.inner_text().strip() if salario_el.count() > 0 else "Faixa salarial não informada nesta vaga"
            
            resultados.append({
                "cargo": titulo,
                "empresa": empresa,
                "salario": salario
            })
            
        return resultados
