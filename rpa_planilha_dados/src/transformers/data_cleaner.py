import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from pathlib import Path

class DataCleaner:
    """Classe especialista em carregar, filtrar e higienizar os dados do Pandas."""
    def __init__(self, pasta_raw: Path):
        self.pasta_raw = pasta_raw

    def processar_dados_brutos(self, nome_arquivo, linhas_para_pular, col_status, valor_status, colunas_data, colunas_texto):
        caminho_csv = self.pasta_raw / nome_arquivo
        print(f"📥 [Cleaner] Lendo arquivo delimitado por ';' do sistema: {nome_arquivo}")
        
        # =====================================================================
        # 🛠️ CORREÇÃO: AJUSTADO O PONTEIRO DO CABEÇALHO COM 'SKIPROWS'
        # =====================================================================
        # O parâmetro skiprows pula as linhas em branco/títulos iniciais (A1) 
        # e faz o Pandas ler a linha A2 como o verdadeiro cabeçalho do arquivo.
        df = pd.read_csv(
            str(caminho_csv), 
            sep=';', 
            encoding='iso-8859-1', 
            dtype=str, 
            skiprows=linhas_para_pular
        )
        
        # Remove quebras de linha (\n) e espaços invisíveis dos cabeçalhos encontrados
        df.columns = df.columns.astype(str).str.replace(r'[\r\n]+', ' ', regex=True).str.strip()

        # 1. Trava colunas críticas como Texto Puro para evitar perdas de formatação/zeros
        for coluna in colunas_texto:
            coluna_limpa = coluna.strip()
            if coluna_limpa in df.columns:
                df[coluna_limpa] = df[coluna_limpa].fillna("").astype(str).str.strip()

        # 2. Tratamento de data em inglês (YYYY-MM-DD) sem horas
        for col_data in colunas_data:
            col_data_limpa = col_data.strip()
            if col_data_limpa in df.columns:
                print(f"📅 [Cleaner] Convertendo coluna '{col_data_limpa}' para padrão Inglês Puro (YYYY-MM-DD)...")
                df[col_data_limpa] = pd.to_datetime(df[col_data_limpa], errors='coerce')
                df[col_data_limpa] = df[col_data_limpa].dt.strftime('%Y-%m-%d')

        # Substitui marcadores nulos por string vazia ""
        df = df.fillna("")

        # 3. Filtragem Condicional por Status (Ex: 'Vigente')
        col_status_limpa = col_status.strip()
        if col_status_limpa not in df.columns:
            raise KeyError(f"❌ Erro: A coluna de filtro '{col_status_limpa}' não existe nesta planilha. Verifique se o nome está idêntico. Disponíveis: {df.columns.tolist()}")

        print(f"⏳ [Cleaner] Filtrando registros onde a coluna '{col_status_limpa}' contém: '{valor_status}'...")
        df_filtrado = df[df[col_status_limpa].astype(str).str.contains(valor_status, case=False, na=False)].copy()
        
        return df_filtrado
    
