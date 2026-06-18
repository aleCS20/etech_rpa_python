# main.py
import sys
import os
from config import (
    PASTA_SISTEMA_BRUTO, PASTA_TEMPLATE_PADRAO, PASTA_RESULTADO_FINAL,
    ARQUIVO_EXTRAIDO_SISTEMA, ARQUIVO_TEMPLATE_GABARITO, LINHA_DO_CABECALHO_REAL,
    NOME_GUIA_TEMPLATE, COLUNA_STATUS_FILTRO, VALOR_STATUS_DESEJADO, 
    COLUNA_DATA_PARA_INGLES, COLUNAS_FORMATO_TEXTO_PURO
)
from src.transformers.extractor_transformer import ExtractorTransformer
from src.transformers.template_injector import TemplateInjector

def main():
    print("==================================================")
    print("     RPA INDUSTRIAL: PIPELINE DE DADOS (.XLS)     ")
    print("==================================================")

    # Cria as pastas de ambiente automaticamente se não existirem
    for pasta in [PASTA_SISTEMA_BRUTO, PASTA_TEMPLATE_PADRAO, PASTA_RESULTADO_FINAL]:
        os.makedirs(str(pasta), exist_ok=True)

    # Validações estruturais de arquivos locais
    if not (PASTA_SISTEMA_BRUTO / ARQUIVO_EXTRAIDO_SISTEMA).exists():
        print(f" Erro: Coloque a planilha do sistema '{ARQUIVO_EXTRAIDO_SISTEMA}' em '/data/raw/'")
        sys.exit(1)
        
    if not (PASTA_TEMPLATE_PADRAO / ARQUIVO_TEMPLATE_GABARITO).exists():
        print(f" Erro: Coloque a planilha padrão '{ARQUIVO_TEMPLATE_GABARITO}' em '/data/template/'")
        sys.exit(1)

    try:
        # ETAPA 1: Extração e Limpeza em Memória RAM
        extrator = ExtractorTransformer(PASTA_SISTEMA_BRUTO)
        dados_tratados = extrator.extrair_e_tratar_dados(
            nome_arquivo=ARQUIVO_EXTRAIDO_SISTEMA,
            linha_cabecalho=LINHA_DO_CABECALHO_REAL,
            col_status=COLUNA_STATUS_FILTRO,
            valor_status=VALOR_STATUS_DESEJADO,
            col_data=COLUNA_DATA_PARA_INGLES,
            colunas_texto=COLUNAS_FORMATO_TEXTO_PURO
        )

        print(f"\n Total de registros localizados pós-filtro: {len(dados_tratados)} linhas.")

        # ETAPA 2: Injeção por Cópia Física e Sobrescrita Segura no Template .xls
        injetor = TemplateInjector(PASTA_TEMPLATE_PADRAO, PASTA_RESULTADO_FINAL)
        injetor.injetar_dados_no_gabarito(
            nome_template=ARQUIVO_TEMPLATE_GABARITO,
            nome_saida=ARQUIVO_TEMPLATE_GABARITO,  
            nome_guia=NOME_GUIA_TEMPLATE,
            dataframe_dados=dados_tratados
        )

        print("\n ***** RPA FINALIZADO COM 100% DE SUCESSO EM FORMATO LEGADO .XLS *****")

    except Exception as e:
        print(f"\n Falha Crítica na execução da esteira de dados: {e}")

if __name__ == "__main__":
    main()
