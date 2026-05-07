import re

BASE_URL = "https://automationexercise.com"
PRODUCT_URL = f"{BASE_URL}/products"

def parse_price(price_string):
    numbers = re.findall(r'\d+.?\d*', price_string)
    return float(numbers[0]) if numbers else 0.0