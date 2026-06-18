# instalar a biblioteca: pip install xlrd
# instalr a biblioteca: pip install xlwt
# instalar a biblioteca: pip install xlutils
# instalar a biblioteca: pip install openpyxl
# instalar a biblioteca: pip install win32com

# config.py
# config.py
from pathlib import Path

# 1. Caminhos de Pastas e Diretórios Locais
BASE_DIR = Path(__file__).resolve().parent
PASTA_SISTEMA_BRUTO = BASE_DIR / "data" / "raw"
PASTA_TEMPLATE_PADRAO = BASE_DIR / "data" / "template"
PASTA_RESULTADO_FINAL = BASE_DIR / "data" / "processed"

# 2. Nomes dos Arquivos Físicos
ARQUIVO_EXTRAIDO_SISTEMA = "terceirizados-cetem_maiago2024.xls"
ARQUIVO_TEMPLATE_XLSX = "planilha_padrao_envio.xlsx"  # O robô usará este para manter as cores
ARQUIVO_FINAL_XLS = "planilha_padrao_envio.xls"       # O formato que será gerado ao final

# Configuração de linha do cabeçalho
LINHA_DO_CABECALHO_REAL = 0  

# Nome da aba gabarito exigida pela indústria
NOME_GUIA_TEMPLATE = "TAX USER RI"

# Parâmetros de filtragem (Ajuste para o seu cenário real na indústria)
COLUNA_STATUS_FILTRO = "Razão Social da Empresa"
VALOR_STATUS_DESEJADO = "PLANSUL PLANEJAMENTO E CONSULTORIA EIRELI"

COLUNA_DATA_PARA_INGLES = "Data Início da Ação"
COLUNAS_FORMATO_TEXTO_PURO = ["CNPJ", "Código da UG\nUnidade Gestora"]


