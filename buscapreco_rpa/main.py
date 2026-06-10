from playwright.sync_api import sync_playwright
from config import LISTA_COMPRAS, URL_SEFAZ
from src.pages.buscapreco_pages import BuscaPrecoPages
from src.pages.analisapreco_pages import AnalisaPrecoPages

def main():
    print(" ***** RPA SEFAZ: BUSCADOR DE PREÇOS ******* ")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context(
            viewport=None,
            permissions=["geolocation"],
            geolocation={"latitude": -3.1190275, "longitude": -60.0217314}
        )
        page = context.new_page()
        
        bot_crawler = BuscaPrecoPages(page, URL_SEFAZ)
        bot_crawler.abrir_portal()
        
        dados_brutos = bot_crawler.pesquisar_lista_itens(LISTA_COMPRAS)
        
        analisador = AnalisaPrecoPages(dados_brutos)
        
        top3_precos = analisador.obter_top3_por_item()
        melhor_opcao, pior_opcao = analisador.calcular_melhor_e_pior_estabelecimento()
        
        print("\n ******* RELATÓRIO DE ECONOMIA SEFAZ ******* ")
        print(f" Total de Itens Processados: {len(LISTA_COMPRAS)}")
        print(f" Estabelecimento MAIS BARATO para compra geral: {melhor_opcao[0]} (R$ {melhor_opcao[1]['total']:.2f})")
        print(f" Estabelecimento MAIS CARO para compra geral:   {pior_opcao[0]} (R$ {pior_opcao[1]['total']:.2f})")
        print("===============================================\n")
        
        context.close()
        browser.close()

if __name__ == "__main__":
    main()


