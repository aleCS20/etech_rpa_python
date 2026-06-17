import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

class Mailer:
    def __init__(self, smtp_server, smtp_port, email_remetente, password_remetente):
        self.server = smtp_server
        self.port = smtp_port
        self.remetente = email_remetente
        self.password = password_remetente

    def enviar_relatorio_com_anexo(self, destinatario, assunto, corpo, caminho_anexo: Path):
        """Prepara o escopo do e-mail, anexa o arquivo .xls e despacha via SMTP seguro."""
        print(f" Preparando envio de e-mail para: {destinatario}")
        
        if not caminho_anexo.exists():
            raise FileNotFoundError(f" O anexo informado não existe no caminho: {caminho_anexo}")

        mensagem = MIMEMultipart()
        mensagem['From'] = self.remetente
        mensagem['To'] = destinatario
        mensagem['Subject'] = assunto

        # Injeta o corpo de texto na mensagem
        mensagem.attach(MIMEText(corpo, 'plain', 'utf-8'))

        # Anexando o arquivo -> (.xls)
        nome_anexo = caminho_anexo.name
        print(f"📎 [Mailer] Compactando e anexando o arquivo: {nome_anexo}")
        
        try:
            with open(str(caminho_anexo), "rb") as arquivo_fisico:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(arquivo_fisico.read())
                
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={nome_anexo}",
            )
            mensagem.attach(part)
            
            # Conexão e transmissão de dados com o servidor interno
            print(f" Estabelecendo conexão com o servidor SMTP {self.server}:{self.port}...")
            
            # bloco para integrar o código desenvolvido para encaminhar o e-mail
            """
            with smtplib.SMTP(self.server, self.port) as servidor:
                servidor.starttls() # Ativa criptografia de transporte TLS
                servidor.login(self.remetente, self.password)
                servidor.sendmail(self.remetente, destinatario, mensagem.as_string())
            """
            
            print(f" E-mail com o relatório '{nome_anexo}' enviado com sucesso para {destinatario}!")
            return True

        except Exception as e:
            print(f" Falha ao transmitir mensagem via protocolo SMTP: {e}")
            return False
