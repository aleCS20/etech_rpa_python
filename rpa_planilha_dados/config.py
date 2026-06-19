# instalar a biblioteca: pip install xlrd
# instalr a biblioteca: pip install xlwt
# instalar a biblioteca: pip install xlutils
# instalar a biblioteca: pip install openpyxl
# instalar a biblioteca: pip install win32com

from pathlib import Path

# =====================================================================
# 🛠️ [ALTERE AQUI NA INDÚSTRIA]: CAMINHOS DAS PASTAS LOCAIS
# =====================================================================
BASE_DIR = Path(__file__).resolve().parent
PASTA_SISTEMA_BRUTO = BASE_DIR / "data" / "raw"
PASTA_TEMPLATE_PADRAO = BASE_DIR / "data" / "template"
PASTA_RESULTADO_FINAL = BASE_DIR / "data" / "processed"

# =====================================================================
# 🛠️ [ALTERE AQUI NA INDÚSTRIA]: NOMES DOS ARQUIVOS FÍSICOS
# =====================================================================
# Altere para os nomes exatos das planilhas que o sistema da fábrica gera.
ARQUIVO_EXTRAIDO_SISTEMA = "patentes-2025.csv"     
ARQUIVO_TEMPLATE_GABARITO = "patentes-template-2025.xlsx"
ARQUIVO_FINAL_ENVIO = "relatorio_final_patentes.xlsx"

# =====================================================================
# 🛠️ [ALTERE AQUI NA INDÚSTRIA]: NOME DA ABA/GUIA DO TEMPLATE
# =====================================================================
# O robô procurará exatamente esta aba para colar os dados.
NOME_GUIA_TEMPLATE = "TAX USER (RI)"

# =====================================================================
# 🛠️ [ALTERE AQUI NA INDÚSTRIA]: AJUSTE DE LINHA DO CABEÇALHO
# =====================================================================
# No laboratório (Patentes), os títulos reais começam na linha 2 (A2),
# então pulamos 1 linha (skiprows=1). 
# Se no sistema real da indústria o cabeçalho começar direto na primeira
# linha (A1), mude o valor abaixo para: 0
PULAR_LINHAS_BRUTAS = 1

# =====================================================================
# 🛠️ [ALTERE AQUI NA INDÚSTRIA]: COLUNA E CRITÉRIO DE FILTRAGEM
# =====================================================================
# Mude para o nome da coluna de status e o valor (Ex: 'Status' e 'Aprovado')
COLUNA_STATUS_FILTRO = "SITUAÇÃO"                
VALOR_STATUS_DESEJADO = "Vigente"                  

# =====================================================================
# 🛠️ [ALTERE AQUI NA INDÚSTRIA]: COLUNAS DE DATA PARA FORMATO INGLÊS
# =====================================================================
# Insira aqui todas as colunas que precisam ir para o padrão YYYY-MM-DD sem horas.
COLUNAS_DATA_PARA_INGLES = ["Data de Depósito", "Data de Validade da Patente"]

# =====================================================================
# 🛠️ [ALTERE AQUI NA INDÚSTRIA]: COLUNAS PARA TRAVAR COMO TEXTO PURO
# =====================================================================
# Adicione aqui os campos numéricos que o Excel costuma cortar zeros (Ex: CNPJ, Código)
COLUNAS_FORMATO_TEXTO_PURO = ["Pedido", "Número da Revista"]
