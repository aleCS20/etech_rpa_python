from src.scraper import ProductScraper
from src.persistence import DataPersistence
from src.processor import ProductProcessor

def run_challenge():
    url = "https://automationexercise.com/products"
    
    # 1. Extração de dados
    scraper = ProductScraper(url)
    produtos = scraper.get_products()
    print(f"🔎 Total de produtos encontrados: {len(produtos)}")

    # 2. Persistência de dados para salvar em .csv
    DataPersistence.save_to_csv(produtos, "data", "produtos.csv")

    # 3. Análise dos valores maior e menor
    max_p, min_p = ProductProcessor.get_price_extremes(produtos)
    
    if (max_p and min_p):
        print(f"\n📈 Maior Valor: {max_p['nome']} - {max_p['preco']}")
        print(f"📉 Menor Valor: {min_p['nome']} - {min_p['preco']}")

if __name__ == "__main__":
    run_challenge()
