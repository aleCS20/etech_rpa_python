import os
from src.utils.constants import Constants

class BotCityLoginPage:
    def __init__(self, page):
        self.page = page
        self.email_input = page.get_by_placeholder("Email")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def acessar_pagina(self):
        self.page.goto(Constants.BOTCITY_LOGIN_URL)

    def realizar_login_manual(self):
        print("⏳ Aguardando login manual no navegador... Faça o login e mude de página.")
        
        self.page.wait_for_url("**/dashboard**", timeout=120000)
        
        os.makedirs("config", exist_ok=True)
        
        self.page.context.storage_state(path=Constants.SESSION_PATH)
        print(f"✅ Sessão salva com sucesso em: {Constants.SESSION_PATH}")

