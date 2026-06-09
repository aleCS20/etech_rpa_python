from playwright.sync_api import sync_playwright
from src.pages.flightradar_page import FlightRadarPage

def main():
    print(" Inicializando Automação -> Flightradar24 ...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport=None)
        page = context.new_page()

        rpa = FlightRadarPage(page)

        rpa.iniciar_navegador()
        rpa.simular_movimento_mapa()

        print("\n === INICIANDO ETAPA DE AVIÕES ===")
        rpa.varrer_e_clicar_aviao(meta_requisito=5)
        
        rpa.deslocar_para_area_de_helicopteros()

        print("\n === INICIANDO ETAPA DE HELICÓPTEROS ===")
        rpa.varrer_e_clicar_helicoptero(meta_requisito=2)

        print(" Finalizando automação em 5 segundos...")
        page.wait_for_timeout(5000)
        context.close()
        browser.close()

if __name__ == "__main__":
    main()
