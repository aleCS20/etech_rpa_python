# instalar a biblioteca: pip install xlrd
# instalr a biblioteca: pip install xlwt
# instalar a biblioteca: pip install xlutils
# instalar a biblioteca: pip install openpyxl

# config.py
from pathlib import Path

# 1. Caminhos de Pastas e Diretórios Locais
BASE_DIR = Path(__file__).resolve().parent
PASTA_SISTEMA_BRUTO = BASE_DIR / "data" / "raw"
PASTA_TEMPLATE_PADRAO = BASE_DIR / "data" / "template"
PASTA_RESULTADO_FINAL = BASE_DIR / "data" / "processed"

# 2. Nomes dos Arquivos Físicos (Todos em formato estrito .xls)
ARQUIVO_EXTRAIDO_SISTEMA = "terceirizados-cetem_maiago2024.xls"
ARQUIVO_TEMPLATE_GABARITO = "planilha_padrao_envio.xls"

# =====================================================================
#  AJUSTE PARA A INDÚSTRIA: LINHA DO CABECALHO REAL
# =====================================================================
# Neste arquivo de teste, os títulos começam logo na linha 1 (índice 0).
# Deixamos configurado como 0. Se na indústria mudar, altere aqui.
LINHA_DO_CABECALHO_REAL = 0  

# Nome da aba gabarito exigida pela indústria
NOME_GUIA_TEMPLATE = "TAX USER RI"

# =====================================================================
#  AJUSTE PARA A INDÚSTRIA: COLUNA E VALOR DE FILTRAGEM (STATUS)
# =====================================================================
# Para o nosso laboratório, usaremos a coluna de Empresa e o valor Plansul.
# Na indústria, altere 'Razão Social da Empresa' para 'Status'
# e 'PLANSUL PLANEJAMENTO...' para 'Aprovado'
COLUNA_STATUS_FILTRO = "Razão Social da Empresa"
VALOR_STATUS_DESEJADO = "PLANSUL PLANEJAMENTO E CONSULTORIA EIRELI"

# Nome do campo de data adicionado para o teste (Formatar para Inglês)
COLUNA_DATA_PARA_INGLES = "Data Início da Ação"

# Liste as colunas que devem manter formato de Texto Estrito (Sem perdas de zeros)
COLUNAS_FORMATO_TEXTO_PURO = ["CNPJ", "Código da UG\nUnidade Gestora"]

