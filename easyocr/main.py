import os
from src.pages.comprovante_easyocr import ComprovanteEasyProcessor

def run_ocr_pipeline():
    NOME_COMPROVANTE = "assets/comprovante.jpg"

    print("==================================================")
    print("       RPA DATA EXTRACTION: PIPELINE EASYOCR      ")
    print("==================================================")

    if not os.path.exists(NOME_COMPROVANTE):
        print(f" Erro: Coloque o arquivo '{NOME_COMPROVANTE}' na raiz do seu projeto antes de rodar.")
        return

    try:
        processador = ComprovanteEasyProcessor(idiomas=["pt"])
        dados_extraidos = processador.extrair_dados_lista(NOME_COMPROVANTE)

        print("\n --- TEXTOS DETECTADOS NO COMPROVANTE (ORDENADOS) ---")
        print("-" * 55)
        if not dados_extraidos:
            print(" Nenhuma informação legível foi detectada na imagem.")
        else:
            for indice, linha in enumerate(dados_extraidos, 1):
                print(f" [Linha {indice:02d}]: {linha}")
        print("-" * 55)
        print(" Processamento de imagem finalizado com sucesso!")

    except Exception as e:
        print(f" Falha crítica no processamento da pipeline: {e}")

if __name__ == "__main__":
    run_ocr_pipeline()
