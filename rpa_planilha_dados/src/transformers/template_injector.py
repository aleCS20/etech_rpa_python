# src/transformers/template_injector.py
import xlrd
import xlwt
from xlutils.copy import copy
import pandas as pd
from pathlib import Path

class TemplateInjector:
    def __init__(self, pasta_template: Path, pasta_destino: Path):
        self.pasta_template = pasta_template
        self.pasta_destino = pasta_destino

    def injetar_dados_no_gabarito(self, nome_template, nome_saida, nome_guia, dataframe_dados):
        """Abre a planilha padrão .xls e injeta os dados garantindo a preservação total de estilos e grades."""
        caminho_template = self.pasta_template / nome_template
        caminho_saida = self.pasta_destino / nome_saida

        print(f"📋 [Injector] Carregando a Planilha Padrão Gabarito: {nome_template}")
        
        # Carrega o arquivo com todas as propriedades de formatação globais ativas
        rb = xlrd.open_workbook(str(caminho_template), formatting_info=True)
        
        idx_aba = None
        for idx, sheet_name in enumerate(rb.sheet_names()):
            if sheet_name == nome_guia:
                idx_aba = idx
                break
        
        if idx_aba is None:
            print(f"⚠️ Aba '{nome_guia}' não localizada. Usando a primeira guia do arquivo.")
            idx_aba = 0

        aba_leitura = rb.sheet_by_index(idx_aba)
        max_linhas_antigas = aba_leitura.nrows

        # Clona o arquivo base mantendo a integridade das tabelas PALETTE e FONT
        wb = copy(rb)
        aba_escrita = wb.get_sheet(idx_aba)

        # Copia explicitamente a largura de todas as colunas mapeadas no template
        for col_idx in range(aba_leitura.ncols):
            if col_idx in aba_leitura.colinfo_map:
                largura_original = aba_leitura.colinfo_map[col_idx].width
                aba_escrita.col(col_idx).width = largura_original

        print(f"⚡ [Injector] Gravando dados e aplicando estilos estruturais na aba '{nome_guia}'...")
        
        cabecalhos = dataframe_dados.columns.tolist()
        
        # Converte a matriz de dados para tipos primitivos
        registros_puros = []
        for row in dataframe_dados.values.tolist():
            linha_limpa = []
            for celula in row:
                # CORREÇÃO DE GRADE: Se for nulo ou vazio, mantém um caractere de espaço
                # para forçar o xlwt a renderizar as bordas e alinhamentos da célula
                if pd.isna(celula) or str(celula).lower() == "nan" or str(celula).strip() == "":
                    linha_limpa.append(" ")
                else:
                    linha_limpa.append(str(celula).strip())
            registros_puros.append(linha_limpa)

        # 1. Escrita Preservando o Cabeçalho (Linha 0)
        for col_idx, nome_coluna in enumerate(cabecalhos):
            try:
                estilo_xf_index = aba_leitura.cell_xf_index(0, col_idx)
                aba_escrita.write(0, col_idx, nome_coluna)
                aba_escrita.get_cell_config(0, col_idx).xf_index = estilo_xf_index
            except Exception:
                aba_escrita.write(0, col_idx, nome_coluna)

        # 2. Injeção Sequencial das Linhas Aplicando o xf_index do Modelo
        linha_atual = 1
        for linha_dados in registros_puros:
            for col_idx, valor in enumerate(linha_dados):
                try:
                    # Captura o design exato da linha de dados modelo do template (Linha 1)
                    estilo_xf_index = aba_leitura.cell_xf_index(1, col_idx)
                    
                    # Força a escrita e amarra o índice de estilo diretamente no bloco de célula
                    aba_escrita.write(linha_atual, col_idx, valor)
                    aba_escrita.get_cell_config(linha_atual, col_idx).xf_index = estilo_xf_index
                except Exception:
                    aba_escrita.write(linha_atual, col_idx, valor)
            linha_atual += 1

        # 3. Limpeza Ativa de Sobras Antigas Mantendo o Layout Visual de Grades
        if max_linhas_antigas > linha_atual:
            print("🧹 [Injector] Removendo registros antigos remanescentes do template...")
            for r_idx in range(max_linhas_antigas - 1, linha_atual - 1, -1):
                try:
                    for col_idx in range(aba_leitura.ncols):
                        # Pega o estilo padrão que estava naquela linha antiga para não perder a borda ao limpar
                        estilo_xf_index = aba_leitura.cell_xf_index(r_idx, col_idx)
                        aba_escrita.write(r_idx, col_idx, " ")
                        aba_escrita.get_cell_config(r_idx, col_idx).xf_index = estilo_xf_index
                    aba_escrita.row(r_idx).collapse = True
                except Exception:
                    pass

        # 4. Salvamento físico final do binário .xls
        print(f"💾 [Injector] Gravando relatório final estruturado em: /processed/{nome_saida}")
        wb.save(str(caminho_saida))
        print("✅ [Injector] Processamento, alinhamento e grades finalizados com sucesso!")
