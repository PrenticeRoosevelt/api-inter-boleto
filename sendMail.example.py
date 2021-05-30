import smtplib
import email
import email.mime.application, email.mime.multipart, email.mime.text

# Configuração de conexão
smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465
username = 'user-auth@gmail.com'
password = 'x1x2x3x4x5'
from_addr = 'remetente@gmail.com'
msg = email.mime.multipart.MIMEMultipart()

def envioEmail(emailTo, condomino, vencimento, boletoAnexo):
    try:
        msg['From'] = from_addr
        msg['To'] = emailTo
        msg['Subject'] = "Assunto da mensagem "+vencimento
        body = email.mime.text.MIMEText("Prezado(a) "+condomino+", \nSegue anexo o boleto do condominio.")
        msg.attach(body)

        # Anexando o PDF
        pdfname=boletoAnexo
        fp=open(pdfname,'rb')
        anexo = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
        fp.close()
        anexo.add_header('Content-Disposition','attachment',filename=pdfname)
        msg.attach(anexo)

        # Enviando via "fake" server 
        s = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        s.login(username, password)
        s.sendmail(username,[emailTo], msg.as_string())
        s.quit()
        print ("E-mail enviado com sucesso")
    except:
        print ("Erro ao enviar e-mail")
        return s
