from src.scraper import ProductScraper
from src.persistence import DataPersistence
from src.processor import ProductProcessor
from src.view import ProductView
from src.utils.utils import PRODUCT_URL

def run_challenge():
    
    scraper = ProductScraper(PRODUCT_URL)
    produtos = scraper.get_products()
    
    max_p, min_p = ProductProcessor.get_extremes(produtos)

    if produtos:
        DataPersistence.save_to_csv(produtos, "data", "produtos.csv")
    
    ProductView.exibir_relatorio(produtos, max_p, min_p)

if __name__ == "__main__":
    run_challenge()
