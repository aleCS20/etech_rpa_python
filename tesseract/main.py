from src.pages.humanbench_test import HumanBenchTest
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        rpa = HumanBenchTest(page)

        rpa.open_browser()
        rpa.clicar_reaction_time_test()
        rpa.clicar_wait_estart()
        
        print("Encerrando Automação...")
        browser.close()

if __name__ == "__main__":
    main()

