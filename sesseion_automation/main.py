import os
from playwright.sync_api import sync_playwright
from src.pages.login_page import BotCityLoginPage
from src.utils.constants import Constants

def executar_rpa_botcity():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        if not os.path.exists(Constants.SESSION_PATH):
            print("Primeira execução: Sessão não encontrada. Iniciando login manual...")
            
            context = browser.new_page()
            bot_page = BotCityLoginPage(context)
            
            bot_page.acessar_pagina()
            bot_page.realizar_login_manual()
            
            context.close()
        
        print("\nSegunda execução (ou recorrente): Reutilizando sessão salva...")
        
        authenticated_context = browser.new_context(storage_state=Constants.SESSION_PATH)
        page = authenticated_context.new_page()
        
        page.goto("https://developers.botcity.dev/dashboard")
        
        print("Validando se o acesso foi direto...")
        page.wait_for_load_state("networkidle")
        
        print(f"URL Atual: {page.url}")
        print("Logado via Session com sucesso!")
        
        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    executar_rpa_botcity()
