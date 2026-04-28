import re

class ProductProcessor:
    @staticmethod
    def get_price_extremes(products):
        if not products:
            return None, None

        def extract_value(price_string):
            """Extrai apenas os números e pontos de uma string como 'Rs. 500'"""
            numbers_only = re.findall(r'\d+\.?\d*', price_string)
            
            return float(numbers_only[0]) if numbers_only else 0.0

        max_product = max(products, key=lambda p: extract_value(p['preco']))
        min_product = min(products, key=lambda p: extract_value(p['preco']))
        
        return max_product, min_product

