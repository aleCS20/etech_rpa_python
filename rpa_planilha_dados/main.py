# main.py
import sys
from config import (
    DATA_RAW_DIR, DATA_PROCESSED_DIR, ARQUIVO_TREINO,
    SMTP_SERVER, SMTP_PORT, EMAIL_REMETENTE, PASSWORD_REMETENTE, EMAIL_DESTINATARIO
)
from src.transformers.excel_transformer import ExcelTransformer
from src.utils.mailer import Mailer

def main():
    print("***** EXECUTANDO O RPA DE TRATAMENTO DE PLANILHAS *****\n")
    
    # Validação de Segurança de Entrada
    arquivo_bruto = DATA_RAW_DIR / ARQUIVO_TREINO
    if not arquivo_bruto.exists():
        print(f" Erro de Entrada: Coloque a planilha '{ARQUIVO_TREINO}' em '/data/raw/' para rodar o teste.")
        sys.exit(1)

    try:
        # ETAPA 1: Instanciação e Execução do Tratamento da Planilha
        processador = ExcelTransformer(DATA_RAW_DIR, DATA_PROCESSED_DIR)
        caminho_planilha_tratada = processador.tratar_planilha_industrial(ARQUIVO_TREINO)
        
        print("\n-------------------------------------------------------------")
       
        # ETAPA 2: Instanciação e Execução do Envio de E-mail
        #bot_email = Mailer(SMTP_SERVER, SMTP_PORT, EMAIL_REMETENTE, PASSWORD_REMETENTE)
        
        #assunto_rpa = "RPA: Relatório Industrial CNPq Tratado (Até 15ª Edição)"
        '''corpo_rpa = (
            "Olá Gestor,\n\n"
            "Segue em anexo o relatório extraído do sistema interno devidamente processado pelo RPA.\n"
            "As colunas Categoria e Classificação foram removidas e os dados limitados à 15ª edição.\n\n"
            "Atenciosamente,\nRobô de Processos Industriais."
        )'''
        '''
        bot_email.enviar_relatorio_com_anexo(
            destinatario=EMAIL_DESTINATARIO,
            assunto=assunto_rpa,
            corpo=corpo_rpa,
            caminho_anexo=caminho_planilha_tratada
        )'''
        
        print("\n ***** AUTOMAÇÃO EXECUTADA COM SUCESSO *****")

    except Exception as e:
        print(f"\n Falha Geral do RPA -> : {e}")

if __name__ == "__main__":
    main()
