from playwright.sync_api import sync_playwright
from src.pages.robo_aiming import RoboAiminig

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        robo = RoboAiminig(page)
        robo.abrir_navegador_site()
        robo.start_game()
        robo.fire_ball()
        robo.finalizar_jogo()

        browser.close()

if __name__ == '__main__':
    main()

