# src/transformers/extractor_transformer.py
import pandas as pd
from pathlib import Path

class ExtractorTransformer:
    def __init__(self, pasta_origem: Path):
        self.pasta_origem = pasta_origem

    def extrair_e_tratar_dados(self, nome_arquivo, linha_cabecalho, col_status, valor_status, col_data, colunas_texto):
        """Lê o arquivo .xls do sistema, trata tipos e filtra dados em memória."""
        caminho_completo = self.pasta_origem / nome_arquivo
        print(f" 📥 [Extractor] Abrindo planilha do sistema via xlrd: {nome_arquivo}")

        # Carga forçada via engine antiga e segura xlrd
        df = pd.read_excel(str(caminho_completo), engine='xlrd', header=linha_cabecalho, dtype=str)
        
        # =====================================================================
        # 🛠️ CORREÇÃO CRÍTICA: LIMPEZA ULTRA AGRESSIVA DE CABEÇALHOS
        # =====================================================================
        # Remove quebras de linha (\n), retornos de carro (\r) e espaços extras 
        # que impediam o script de encontrar as colunas de data e status.
        df.columns = df.columns.astype(str).str.replace(r'[\r\n]+', ' ', regex=True).str.strip()
        print(f"   ↳ Cabeçalhos normalizados com sucesso.")

        # Tratamento de segurança anti-corrupção para campos de texto/identificadores
        print(f" 🔤 [Extractor] Forçando colunas de códigos para formato de Texto Puro...")
        for coluna in colunas_texto:
            coluna_limpa = coluna.replace('\n', ' ').strip()
            if coluna_limpa in df.columns:
                df[coluna_limpa] = df[coluna_limpa].fillna("").astype(str)
                df[coluna_limpa] = df[coluna_limpa].str.replace(".0", "", regex=False).str.strip()

        # Converte e padroniza a data para o formato inglês (YYYY-MM-DD)
        col_data_limpa = col_data.replace('\n', ' ').strip()
        if col_data_limpa in df.columns:
            print(f" 📅 [Extractor] Convertendo coluna '{col_data_limpa}' para formato Inglês Puro...")
            df[col_data_limpa] = pd.to_datetime(df[col_data_limpa], errors='coerce')
            df[col_data_limpa] = df[col_data_limpa].dt.strftime('%Y-%m-%d')
            df[col_data_limpa] = df[col_data_limpa].fillna("")
        else:
            print(f" ⚠️ [Extractor] Aviso: Coluna de data '{col_data_limpa}' não foi processada pois não foi encontrada.")

        # Aplica a filtragem condicional pelo Status (ou Empresa no laboratório)
        col_status_limpa = col_status.replace('\n', ' ').strip()
        if col_status_limpa not in df.columns:
            raise KeyError(f"❌ Erro Crítico: A coluna de filtro '{col_status_limpa}' não existe nesta planilha. Disponíveis: {df.columns.tolist()}")

        print(f" ⏳ [Extractor] Filtrando registros onde a coluna contêm: '{valor_status}'...")
        
        # Garante que a coluna de status não tenha nulos antes do filtro de texto
        df[col_status_limpa] = df[col_status_limpa].fillna("").astype(str).str.strip()
        df_filtrado = df[df[col_status_limpa].str.contains(valor_status, case=False, na=False)].copy()

        # Finalização de segurança: garante que NENHUM campo nulo do pandas (NaN/None) vá para a matriz pura
        df_filtrado = df_filtrado.fillna("")

        return df_filtrado
    