# src/transformers/excel_transformer.py
import xlrd
import xlwt
from xlutils.copy import copy
import re
from pathlib import Path

class ExcelTransformer:
    def __init__(self, pasta_origem: Path, pasta_destino: Path):
        self.pasta_origem = pasta_origem
        self.pasta_destino = pasta_destino

    def tratar_planilha_industrial(self, nome_arquivo):
        caminho_entrada = self.pasta_origem / nome_arquivo
        caminho_saida = self.pasta_destino / nome_arquivo

        print(f" Espelhando arquivo e estilos via xlrd + xlutils: {nome_arquivo}")
        
        # 1. Abre o arquivo original mantendo a formatação viva na memória do xlrd
        rb = xlrd.open_workbook(str(caminho_entrada), formatting_info=True)
        
        # 2. Faz uma cópia idêntica do arquivo incluindo fontes, larguras, cores e bordas
        wb = copy(rb)
        
        # Seleciona a primeira aba para leitura (rb) e para escrita (wb)
        aba_leitura = rb.sheet_by_index(0)
        aba_escrita = wb.get_sheet(0)

        # 3. Mapeia a posição das colunas pelos nomes do cabeçalho (linha 0)
        cabecalho = [aba_leitura.cell_value(0, col) for col in range(aba_leitura.ncols)]
        
        try:
            idx_edicao = cabecalho.index("Edição")
            idx_categoria = cabecalho.index("Categoria") if "Categoria" in cabecalho else None
            idx_classificacao = cabecalho.index("Classificação") if "Classificação" in cabecalho else None
        except ValueError as e:
            raise KeyError(f" Coluna essencial não localizada no cabeçalho: {e}")

        # Função interna para limpar a string da edição (ex: "14ª" -> 14)
        def extrair_numero_edicao(texto):
            numeros = re.findall(r'\d+', str(texto))
            return int(numeros[0]) if numeros else 0

        print(" Aplicando regras de negócio diretamente nas células formatadas...")
        
        # 4. Varre as linhas de baixo para cima (da última até a linha 1)
        # Nota: Varremos de trás para frente para que a limpeza de registros não mude o índice das linhas anteriores
        linhas_mantidas = 0
        linhas_eliminadas = 0

        # Criamos uma nova folha limpa caso queira reescrever, mas a melhor forma de manter 
        # a estrutura sem perder formatação de células vazias é limpar o conteúdo indesejado:
        for row_idx in range(1, aba_leitura.nrows):
            valor_edicao = aba_leitura.cell_value(row_idx, idx_edicao)
            num_edicao = extrair_numero_edicao(valor_edicao)
            
            # REQUISITO 1: Se a edição for maior que 15, limpamos a linha inteira
            if num_edicao > 15:
                linhas_eliminadas += 1
                for col_idx in range(aba_leitura.ncols):
                    aba_escrita.write(row_idx, col_idx, "") # Remove o dado mas mantém a célula lá estruturada
            else:
                linhas_mantidas += 1
                # REQUISITO 2: Se a linha for válida, limpamos apenas as colunas Categoria e Classificação
                if idx_categoria is not None:
                    aba_escrita.write(row_idx, idx_categoria, "")
                if idx_classificacao is not None:
                    aba_escrita.write(row_idx, idx_classificacao, "")

        # 5. Grava o arquivo binário final preservando o esqueleto de estilos original do Nginx/Sistema
        print(f" Gravando planilha com formatação preservada em: /processed/{nome_arquivo}")
        wb.save(str(caminho_saida))
        
        print(f" Filtro concluído! Mantidos: {linhas_mantidas} | Removidos: {linhas_eliminadas}")
        return caminho_saida
