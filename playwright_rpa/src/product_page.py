class ProductPage:
    def __init__(self, page):
        self.page = page
        self.products_locator = page.locator(".productinfo p")
        self.price_locator = page.locator(".productinfo h2")

    def navegar(self):
        self.page.goto("https://automationexercise.com/products")
    
    def coletar_e_imprimir_produtos(self):
        count = self.products_locator.count()
    
        print(f"🔎 Total de produtos encontrados: {count}")
    
        for i in range(count):
            nome = self.products_locator.nth(i).inner_text()
            preco = self.price_locator.nth(i).inner_text()
            print(f"Item {i+1}: {nome} - Valor: {preco}")

