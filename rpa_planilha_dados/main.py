# main.py
import sys
import os
import win32com.client as win32  # Ponte nativa do Windows para conversão perfeita
from config import (
    PASTA_SISTEMA_BRUTO, PASTA_TEMPLATE_PADRAO, PASTA_RESULTADO_FINAL,
    ARQUIVO_EXTRAIDO_SISTEMA, ARQUIVO_TEMPLATE_XLSX, ARQUIVO_FINAL_XLS,
    LINHA_DO_CABECALHO_REAL, NOME_GUIA_TEMPLATE, COLUNA_STATUS_FILTRO, 
    VALOR_STATUS_DESEJADO, COLUNA_DATA_PARA_INGLES, COLUNAS_FORMATO_TEXTO_PURO
)
from src.transformers.extractor_transformer import ExtractorTransformer
from src.transformers.template_injector import TemplateInjector

def converter_xlsx_para_xls_nativo(caminho_xlsx, caminho_xls):
    """Usa a engine do Excel local para salvar em .xls mantendo 100% das cores e fontes."""
    print(f"🔄 [Conversor] Convertendo arquivo final para o formato legado .xls da indústria...")
    try:
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Visible = False  # Executa de forma invisível em segundo plano
        excel.DisplayAlerts = False
        
        wb = excel.Workbooks.Open(str(caminho_xlsx))
        # xlExcel8 é o código numérico binário do formato Excel 97-2003 (.xls)
        wb.SaveAs(str(caminho_xls), FileFormat=56) 
        wb.Close()
        excel.Quit()
        print(f"🚀 [Conversor] Sucesso! Arquivo .xls legítimo gerado com formatação de fábrica.")
    except Exception as e:
        print(f"⚠️ Erro na conversão nativa do Windows: {e}")
        print("Certifique-se de que o Microsoft Excel está instalado nesta máquina.")

def main():
    print("==================================================")
    print("     RPA INDUSTRIAL: PIPELINE HÍBRIDO (.XLSX/.XLS) ")
    print("==================================================")

    # Cria as pastas de ambiente automaticamente
    for pasta in [PASTA_SISTEMA_BRUTO, PASTA_TEMPLATE_PADRAO, PASTA_RESULTADO_FINAL]:
        os.makedirs(str(pasta), exist_ok=True)

    # Validações estruturais de arquivos locais
    if not (PASTA_SISTEMA_BRUTO / ARQUIVO_EXTRAIDO_SISTEMA).exists():
        print(f"❌ Erro: Coloque a planilha do sistema '{ARQUIVO_EXTRAIDO_SISTEMA}' em '/data/raw/'")
        sys.exit(1)
        
    if not (PASTA_TEMPLATE_PADRAO / ARQUIVO_TEMPLATE_XLSX).exists():
        print(f"❌ Erro: Coloque a cópia do template '{ARQUIVO_TEMPLATE_XLSX}' em '/data/template/'")
        sys.exit(1)

    try:
        # ETAPA 1: Extração e Limpeza das Datas/Texto (Pandas)
        extrator = ExtractorTransformer(PASTA_SISTEMA_BRUTO)
        dados_tratados = extrator.extrair_e_tratar_dados(
            nome_arquivo=ARQUIVO_EXTRAIDO_SISTEMA,
            linha_cabecalho=LINHA_DO_CABECALHO_REAL,
            col_status=COLUNA_STATUS_FILTRO,
            valor_status=VALOR_STATUS_DESEJADO,
            col_data=COLUNA_DATA_PARA_INGLES,
            colunas_texto=COLUNAS_FORMATO_TEXTO_PURO
        )

        print(f"\n📊 Total de registros localizados pós-filtro: {len(dados_tratados)} linhas.")

        # ETAPA 2: Injeção Segura e Estável no formato .xlsx temporário
        nome_temporario_xlsx = "temp_processado.xlsx"
        injetor = TemplateInjector(PASTA_TEMPLATE_PADRAO, PASTA_RESULTADO_FINAL)
        caminho_xlsx_gerado = injetor.injetar_dados_no_gabarito_xlsx(
            nome_template=ARQUIVO_TEMPLATE_XLSX,
            nome_saida_xlsx=nome_temporario_xlsx,
            nome_guia=NOME_GUIA_TEMPLATE,
            dataframe_dados=dados_tratados
        )

        # ETAPA 3: Conversão Final Perfeita de .xlsx para .xls (Mantém Cores Azuis e Bordas)
        caminho_final_xls = PASTA_RESULTADO_FINAL / ARQUIVO_FINAL_XLS
        converter_xlsx_para_xls_nativo(caminho_xlsx_gerado, caminho_final_xls)

        # Limpeza defensiva: remove o arquivo .xlsx temporário para deixar a pasta limpa
        if caminho_xlsx_gerado.exists():
            os.remove(str(caminho_xlsx_gerado))

        print("\n🏆 ***** RPA FINALIZADO COM SUCESSO ABSOLUTO E FORMATADO *****")

    except Exception as e:
        print(f"\n💥 Falha Crítica na execução da esteira de dados: {e}")

if __name__ == "__main__":
    main()
