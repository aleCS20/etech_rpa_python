import requests
from bs4 import BeautifulSoup

class ProductScraper:
    def __init__(self, url):
        self.url = url
        self.base_url = "https://automationexercise.com"

    def get_products(self):
        response = requests.get(self.url, timeout=10)
        if (response.status_code != 200):
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        product_list = []

        cards = soup.select(".product-image-wrapper")

        for card in cards:
            name_el = card.select_one(".productinfo p")
            price_el = card.select_one(".productinfo h2")
            button_el = card.select_one("a.add-to-cart")
            link_el = card.select_one(".choose a")

            if name_el and price_el and button_el:
                product_list.append({
                    "id": button_el.get("data-product-id"),
                    "nome": name_el.get_text(strip=True),
                    "preco": price_el.get_text(strip=True),
                    "link": self.base_url + link_el.get("href") if link_el else "N/A"
                })
        return product_list
