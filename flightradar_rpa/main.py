from playwright.sync_api import sync_playwright
from src.pages.flightradar_page import FlightRadarPage

def main():
    print(" Inicializando Motor da Automação ...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport=None)
        page = context.new_page()

        rpa = FlightRadarPage(page)

        rpa.iniciar_navegador()
        rpa.varrer_e_clicar_aviao()

        print(" Finalizando automação em 5 segundos...")
        page.wait_for_timeout(5000)
        context.close()
        browser.close()

if __name__ == "__main__":
    main()
