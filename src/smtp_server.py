# IMPORTAÇÕES 

import smtplib
import random
import os 
import PySimpleGUI as sg
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Carregando as variáveis de ambiente
load_dotenv()

class SmtpServer:
    def __init__(self, host, port):
        self.server = smtplib.SMTP(host, port)
        self.email_message = MIMEMultipart()
        self.email_smtp = os.getenv("SMTPEMAIL")
        self.password_smpt = os.getenv("SMTPPASS")

    # Gerador de código de 4 dígitos 
    def code_generator(self):
        char_list = "ABCDEFGHIJKLMNOPQRSUVXWYZ0123456789"
        chars = random.choices(char_list, k=4)
        news_chars = "".join(chars)
        return news_chars
        
    # Função para enviar email para o usuário
    def send_email(self, to_stmp_email):
        self.body = f"{self.code_generator()}"

        #Configurações de email
        self.email_message["From"] = self.email_smtp
        self.email_message["To"] = to_stmp_email
        self.email_message["Subject"] = "Código de alteração de senha"
        self.email_message.attach(MIMEText(self.body,"plain"))

        try:
            # Startando servidor STMP
            self.server.starttls()
            self.server.login(self.email_smtp, self.password_smpt)

            # Enviando o email tipo MIME no servidro SMTP
            self.server.sendmail(self.email_message["From"], self.email_message["To"], self.email_message.as_string())

        except Exception as error:
            print(f"Erro {error}")

        else:
            # Fechando o servidor       
            self.server.quit()
