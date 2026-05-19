from src.utils.config import Config

class LinkedinLoginPage:
    def __init__(self, page):
        self.page = page
        self.email_input = page.get_by_label("E-mail ou número de telefone")
        self.password_input = page.get_by_label("Senha", exact=True)
        self.login_button = page.get_by_role("button", name="Entrar", exact=True)

    def acessar_pagina(self):
        self.page.goto(Config.LINKEDIN_URL)

    def realizar_login(self, email, senha):
        print(f"Efetuando login via credenciais seguras do .env para: {email}")
        self.email_input.fill(email)
        self.password_input.fill(senha)
        self.login_button.click()
        self.page.wait_for_url("**/feed/**", timeout=30000)
        print("Autenticado com sucesso!")
