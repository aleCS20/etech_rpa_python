from playwright.sync_api import Page

class DashboardPage:
       
    def __init__(self, page: Page):
        self.page = page
        self.link_logout = page.locator("a[href='/logout']")

    def esta_autenticado(self) -> bool:
        return self.link_logout.is_visible()

    def obter_html_da_pagina(self) -> str:
        return self.page.content()
    


