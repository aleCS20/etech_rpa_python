
import sys
import os
from config import (
    PASTA_SISTEMA_BRUTO, PASTA_TEMPLATE_PADRAO, PASTA_RESULTADO_FINAL,
    ARQUIVO_EXTRAIDO_SISTEMA, ARQUIVO_TEMPLATE_GABARITO, ARQUIVO_FINAL_ENVIO,
    NOME_GUIA_TEMPLATE, COLUNA_STATUS_FILTRO, VALOR_STATUS_DESEJADO, 
    COLUNAS_DATA_PARA_INGLES, COLUNAS_FORMATO_TEXTO_PURO, PULAR_LINHAS_BRUTAS
)
from src.transformers.data_cleaner import DataCleaner
from src.transformers.excel_injector import ExcelInjector

def main():
    print("==================================================")
    print("     RPA INDUSTRIAL: CORE PIPELINE DO DESAFIO     ")
    print("==================================================")

    # Cria as pastas de ambiente automaticamente caso não existam
    for pasta in [PASTA_SISTEMA_BRUTO, PASTA_TEMPLATE_PADRAO, PASTA_RESULTADO_FINAL]:
        os.makedirs(str(pasta), exist_ok=True)

    # Validações defensivas de presença de arquivos
    if not (PASTA_SISTEMA_BRUTO / ARQUIVO_EXTRAIDO_SISTEMA).exists():
        print(f"❌ Erro de Entrada: Coloque o arquivo de dados '{ARQUIVO_EXTRAIDO_SISTEMA}' em '/data/raw/'")
        sys.exit(1)
        
    if not (PASTA_TEMPLATE_PADRAO / ARQUIVO_TEMPLATE_GABARITO).exists():
        print(f"❌ Erro de Template: Coloque a planilha gabarito '{ARQUIVO_TEMPLATE_GABARITO}' em '/data/template/'")
        sys.exit(1)

    try:
        # FASE 1: Instancia o limpador e trata as datas e filtros do Pandas aplicando o skiprows
        limpador = DataCleaner(PASTA_SISTEMA_BRUTO)
        dados_tratados = limpador.processar_dados_brutos(
            nome_arquivo=ARQUIVO_EXTRAIDO_SISTEMA,
            linhas_para_pular=PULAR_LINHAS_BRUTAS, # Injeta o parâmetro de correção
            col_status=COLUNA_STATUS_FILTRO,
            valor_status=VALOR_STATUS_DESEJADO,
            colunas_data=COLUNAS_DATA_PARA_INGLES,
            colunas_texto=COLUNAS_FORMATO_TEXTO_PURO
        )

        print(f"\n📊 Total de registros localizados pós-filtro: {len(dados_tratados)} linhas.")

        # FASE 2: Instancia o injetor e transfere os dados para dentro do template .xlsx
        injetor = ExcelInjector(PASTA_TEMPLATE_PADRAO, PASTA_RESULTADO_FINAL)
        injetor.injetar_no_template_xlsx(
            nome_template=ARQUIVO_TEMPLATE_GABARITO,
            nome_saida=ARQUIVO_FINAL_ENVIO,
            nome_guia=NOME_GUIA_TEMPLATE,
            dataframe_dados=dados_tratados
        )
        
        print("\n🏆 ***** RPA FINALIZADO COM SUCESSO TOTAL NO LABORATORIO *****")

    except Exception as e:
        print(f"\n💥 Falha Crítica na execução do RPA: {e}")

if __name__ == "__main__":
    main()
    
