from playwright.sync_api import sync_playwright
from src.utils.config import Config
from src.pages.login_page import LinkedinLoginPage
from src.pages.salary_page import LinkedinSalaryPage

def executar_desafio_salario():
    print("==================================================")
    print("      RPA LINKEDIN: PESQUISA SALARIAL GLOBAL      ")
    print("==================================================")
    cargo_pesquisa = input("Digite o cargo/vaga desejada (Ex: RPA Developer): ")
    pais_pesquisa = input("Digite o país de destino (Ex: United States ou Canada): ")
    
    if not cargo_pesquisa or not pais_pesquisa:
        print("Erro: O cargo e o país devem ser preenchidos no terminal para continuar.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        page = browser.new_page()

        login = LinkedinLoginPage(page)
        salary_search = LinkedinSalaryPage(page)

        login.acessar_pagina()
        login.realizar_login(Config.EMAIL, Config.PASSWORD)

        salary_search.pesquisar_vagas_internacionais(cargo_pesquisa, pais_pesquisa)
        dados_coletados = salary_search.extrair_estimativas_salariais()

        print(f"\n--- RELATÓRIO SALARIAL: {cargo_pesquisa.upper()} | {pais_pesquisa.upper()} ---")
        print("=" * 60)
        for idx, item in enumerate(dados_coletados, 1):
            print(f" Oportunidade #{idx}")
            print(f"   Função: {item['cargo']}")
            print(f"   Empresa: {item['empresa']}")
            print(f"   Remuneração/Faixa: {item['salario']}")
            print("-" * 60)

        print("Automação finalizada com sucesso!")
        browser.close()

if __name__ == "__main__":
    executar_desafio_salario()
