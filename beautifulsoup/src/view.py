class ProductView:
    @staticmethod
    def exibir_relatorio(produtos, max_p, min_p):
    
        if not produtos:
            print("❌ Nenhum dado foi coletado.")
            return

        print(f"\n✅ Scraping concluído. {len(produtos)} itens capturados.")
        print("-" * 50)

        for idx, p in enumerate(produtos, 1):
            print(f"{idx}. {p['nome']} | Preço: {p['preco']} | ID: {p['id']}")
        
        if max_p and min_p:
            print("\n--- Relatório de Preços ---")
            print(f"💎 Premium: {max_p['nome']} ({max_p['preco']})")
            print(f"🏷️ Econômico: {min_p['nome']} ({min_p['preco']})")

