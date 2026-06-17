# instalar a biblioteca: pip install xlrd
# instalr a biblioteca: pip install xlwt
# instalar a biblioteca: pip install xlutils
import os
from pathlib import Path

# Caminhos dos dados/planilhas
BASE_DIR = Path(__file__).resolve().parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"

os.makedirs(str(DATA_RAW_DIR), exist_ok=True)
os.makedirs(str(DATA_PROCESSED_DIR), exist_ok=True)

# Definições do arquivo baixado e regras de negócio
ARQUIVO_TREINO = "agraciados-cnpq-todos-os-premios-27-07-2022.xls"

# Autenticação do Servidor de E-mail (verificar arquivo .env)
SMTP_SERVER = "smtp.empresa.com.br"
SMTP_PORT = 587
EMAIL_REMETENTE = "rpa.industrial@empresa.com.br"
PASSWORD_REMETENTE = "SenhaSecretaDoBot123"

# Destinatários para encaminhar via e-mail
EMAIL_DESTINATARIO = "gestor.producao@empresa.com.br"

