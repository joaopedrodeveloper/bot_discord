import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def envia_codigo_por_email(email_destino, codigo):
    """Envia codigo por email.
    
    :param email_destino: str
    :param codigo: str
    """

    load_dotenv()
    
    smtp_server = 'smtp.office365.com'  
    smtp_port = 587 
    smtp_usuario = os.getenv('EMAIL')
    smtp_senha = os.getenv('TOKEN_EMAIL') 

    msg = MIMEMultipart()
    msg['From'] = smtp_usuario
    msg['To'] = email_destino  
    msg['Subject'] = 'Código de acesso ao Discord IFPB' 


    body = f'''
    <body style="font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;">
        <div style="display: flex;">
            <div>
                <h3>Olá, segue seu código para liberar seu acesso ao discord IFPB:</h3>
                <h4>Código: <strong>{codigo}</strong></h4>
                <p><strong>ATENÇÃO! Não compartilhe seu código com ninguém.</strong></p>
            </div>
            <div style="width: 100%; text-align: center;">
                <img src="https://www.ifpb.edu.br/imagens/logos/campus-campina-grande" alt="IFPB logo campus Campina Grande" style="width: 100px; height: auto;">
            </div> 
        </div> 
    </body>
    ''' 
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls() 
    server.login(smtp_usuario, smtp_senha)  
    
    server.send_message(msg)
    server.quit()

