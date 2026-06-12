class AnalisaPrecoPages:
    def __init__(self, dados_brutos):
        self.dados = dados_brutos

    def obter_top3_por_item(self):
        resultados_top3 = {}
        
        for item, ofertas in self.dados.items():
            if (not ofertas):
                resultados_top3[item] = []
                continue
            ofertas_ordenadas = sorted(ofertas, key=lambda x: x['preco'])
            resultados_top3[item] = ofertas_ordenadas[:3]
            
        return resultados_top3

    def calcular_melhor_e_pior_estabelecimento(self):
        custo_por_loja = {}

        for item, ofertas in self.dados.items():
            for oferta in ofertas:
                loja = oferta['estabelecimento']
                preco = oferta['preco']
                
                if (not loja or loja == "Não informado"):
                    continue
                
                if (loja not in custo_por_loja):
                    custo_por_loja[loja] = {'total': 0.0, 'itens_encontrados': 0}
                
                custo_por_loja[loja]['total'] += preco
                custo_por_loja[loja]['itens_encontrados'] += 1

        lojas_ordenadas = sorted(custo_por_loja.items(), key=lambda x: x[1]['total'])
        
        if (lojas_ordenadas):
            melhor_loja = lojas_ordenadas[0]
            pior_loja = lojas_ordenadas[-1]
        else:
            estrutura_vazia = {"total": 0.0, "itens_encontrados": 0}
            melhor_loja = ("Sem dados válidos", estrutura_vazia)
            pior_loja = ("Sem dados válidos", estrutura_vazia)
        
        return melhor_loja, pior_loja

