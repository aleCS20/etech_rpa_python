from src.utils.utils import parse_price

class ProductProcessor:
    @staticmethod
    def get_extremes(products):
        if not products:
            return None, None

        max_product = max(products, key=lambda p: parse_price(p['preco']))
        min_product = min(products, key=lambda p: parse_price(p['preco']))
        
        return max_product, min_product

