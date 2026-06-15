from playwright.sync_api import sync_playwright
from config import URL_AUTENTICACAO, USER_RPA, PASSWORD_RPA
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from extractors.scrapy_extractor import BeautifulSoupExtractor

def main():
    print(" ****  DESAFIO FINAL: DESIGN PATTERNS EM RPA  ****  ")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        tela_login = LoginPage(page)
        tela_dashboard = DashboardPage(page)
        
        print(" Acessando ambiente de autenticação...")
        tela_login.acessar_pagina(URL_AUTENTICACAO)
        
        print(" Efetuando preenchimento de credenciais pelo POM...")
        tela_login.executar_login(USER_RPA, PASSWORD_RPA)
        page.wait_for_load_state("domcontentloaded")
        
        if tela_dashboard.esta_autenticado():
            print("Login efetuado com sucesso!")
            html_logado = tela_dashboard.obter_html_da_pagina()
            
            extrator_bs4 = BeautifulSoupExtractor()
            relatorio = extrator_bs4.extrair_relatorio(html_logado)

            print(f"Total de relatórios extraídos com sucesso: {len(relatorio)}")
        else:
            print("Erro: As credenciais inseridas não estão corretas..")
            
        page.wait_for_timeout(3000)
        context.close()
        browser.close()

if __name__ == "__main__":
    main()
