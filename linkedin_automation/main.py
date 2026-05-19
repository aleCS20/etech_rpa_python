from playwright.sync_api import sync_playwright
from src.pages.login_page import LinkedinLoginPage
from src.pages.jobs_page import LinkedinJobsPage

def rodar_rpa_linkedin():
    EMAIL_CONTA = "seu_email@provedor.com"
    SENHA_CONTA = "sua_senha_aqui"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        login_process = LinkedinLoginPage(page)
        jobs_process = LinkedinJobsPage(page)

        login_process.acessar_pagina()
        login_process.realizar_login(EMAIL_CONTA, SENHA_CONTA)

        jobs_process.buscar_vagas()
        vagas_capturadas = jobs_process.coletar_tres_primeiras_vagas()

        print("\nTRÊS PRIMEIRAS VAGAS ENCONTRADAS ---")
        print("-" * 50)
        for vaga in vagas_capturadas:
            print(f"Vaga #{vaga['posicao']}")
            print(f"Cargo: {vaga['titulo']}")
            print(f"Empresa: {vaga['empresa']}")
            print("-" * 50)

        print("Execução terminada com sucesso!")
        browser.close()

if __name__ == "__main__":
    rodar_rpa_linkedin()
