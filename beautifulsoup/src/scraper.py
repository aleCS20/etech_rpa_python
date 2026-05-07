import requests
from bs4 import BeautifulSoup
from src.utils.utils import PRODUCT_URL, BASE_URL

class ProductScraper:
    def __init__(self, url=PRODUCT_URL):
        self.url = url
        self.base_url = BASE_URL

    def _extract_item_data(self, card):
        name = card.select_one(".productinfo p")
        price = card.select_one(".productinfo h2")
        btn = card.select_one("a.add-to-cart")
        link = card.select_one(".choose a")

        if all([name, price, btn]):
            return {
                "id": btn.get("data-product-id"),
                "nome": name.get_text(strip=True),
                "preco": price.get_text(strip=True),
                "link": f"{self.base_url}{link.get('href')}" if link else "N/A"
            }
        return None

    def get_products(self):
        response = requests.get(self.url, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        cards = soup.select(".product-image-wrapper")
        products = [self._extract_item_data(c) for c in cards]

        return [p for p in products if p]

