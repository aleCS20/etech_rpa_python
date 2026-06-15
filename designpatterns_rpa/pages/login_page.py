from playwright.sync_api import Page

class LoginPage:
    
    def __init__(self, page: Page):
        self.page = page
        
        self.input_usuario = page.locator("input#username")
        self.input_senha = page.locator("input#password")
        self.botao_entrar = page.locator("input[type='submit']")

    def acessar_pagina(self, url):
        self.page.goto(url, wait_until="domcontentloaded")

    def executar_login(self, usuario, senha):
        self.input_usuario.fill(usuario)
        self.input_senha.fill(senha)
        self.botao_entrar.click()

