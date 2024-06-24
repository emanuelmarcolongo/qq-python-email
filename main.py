from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class RequestBody(BaseModel):
    email: str
    token: str

def send_reset_email(user_email, token):
    # Configuração do servidor SMTP
    smtp_server = 'smtp.gmail.com'  # Servidor SMTP do Gmail
    smtp_port = 587  # Porta SMTP do Gmail
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')

    # Configuração da mensagem
    from_email = smtp_username
    to_email = user_email
    subject = 'Reset de Senha QQ-Management'
    body = f'Clique no link abaixo para resetar sua senha: localhost:3000/reset-password/{token}'

    # Criando o objeto MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Anexando o corpo do email ao objeto MIME
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conectando ao servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Modo TLS

        # Logando no servidor SMTP
        server.login(smtp_username, smtp_password)

        # Enviando o email
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

        # Encerrando a conexão com o servidor SMTP
        server.quit()

        print('Email sent successfully')
        return True
    except Exception as e:
        print(f'Failed to send email: {e}')
        return False

@app.post("/reset-password/")
async def create_item(request_body: RequestBody):
    email = request_body.email
    token = request_body.token

    if not email or not token:
        raise HTTPException(status_code=400, message="Email ou token não fornecidos")

    email_sent = send_reset_email(email, token)
    
    if not email_sent:
        raise HTTPException(status_code=500, message="Falha ao enviar e-mail")

    return {"message": "Email sent successfully"}