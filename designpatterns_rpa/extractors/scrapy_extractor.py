from bs4 import BeautifulSoup

class ScrapyExtractor:
    
    def extrair_relatorio(self, html_conteudo):
        print(" [Strategy] Iniciando processamento do HTML via BeautifulSoup..")
        soup = BeautifulSoup(html_conteudo, 'html.parser')
        relatorio_final = []
        
        cards_frases = soup.find_all('div', class_='quote')
        
        for card in cards_frases:
            texto = card.find('span', class_='text').get_text().strip()
            autor = card.find('small', class_='author').get_text().strip()
            
            relatorio_final.append({
                "texto": texto,
                "autor": autor
            })
            
        return relatorio_final
