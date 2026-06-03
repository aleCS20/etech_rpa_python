from playwright.sync_api import sync_playwright
from src.pages.flightradar_page import FlightRadarPage as fl

def main():
    print("Iniciando motor RPA...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport=None) 
        page = context.new_page()

        rpa = fl(page)

        rpa.iniciar_navegador()
        rpa.simular_movimento_mapa()
        rpa.selecionar_e_extrair_aeronave()

        print("Aguardando 5 segundos antes de encerrar o sistema...")
        page.wait_for_timeout(5000)

        context.close()
        browser.close()

if __name__ == "__main__":
    main()
    