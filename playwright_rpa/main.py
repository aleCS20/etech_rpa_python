from playwright.sync_api import sync_playwright
from src.product_page import ProductPage

def executar_product_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        rpa = ProductPage(page)

        print("Executando automação... ")

        rpa.navegar()
        rpa.coletar_e_imprimir_produtos()

        print("\nConcluido...\n")
        browser.close()

if __name__ == '__main__':
    executar_product_page()
