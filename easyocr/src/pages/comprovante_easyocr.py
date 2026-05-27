import cv2
import easyocr
import os

class ComprovanteEasyProcessor:
    def __init__(self, idiomas=["pt"]):
        print(" Inicializando redes neurais do EasyOCR...")
        self.reader = easyocr.Reader(idiomas)

    def _pre_processar_imagem(self, caminho_imagem):
        img = cv2.imread(caminho_imagem)
        if img is None:
            raise FileNotFoundError(f" Imagem não encontrada no caminho: {caminho_imagem}")

        img_resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC) 

        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        return thresh

    def extrair_dados_lista(self, caminho_imagem):
        imagem_tratada = self._pre_processar_imagem(caminho_imagem)
        
        print(f" Executando varredura OCR no arquivo '{caminho_imagem}'")

        resultado_ocr = self.reader.readtext(imagem_tratada)

        lista_linhas_texto = []

        for item in resultado_ocr:
            texto = item[1]
            confianca = item[2]
            
            if confianca > 0.30:
                lista_linhas_texto.append(texto.strip()) # [cite: 71]

        return lista_linhas_texto
