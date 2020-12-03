import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os.path


class Email:
    def __init__(self, email, password):
        # https://www.google.com/settings/security/lesssecureapps
        self.email = email
        self.password = password

    def send(self, destinatario, assunto, mensagem, anexos=False, erro=False):
        msg = MIMEMultipart()
        msg["From"] = self.email
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.attach(MIMEText(mensagem, "plain"))

        arquivoAnexo = False

        if anexos != False:
            for anexo in anexos:
                if os.path.isfile(anexo):
                    filename = anexo.split("/")[-1]
                    attachment = open(anexo, "rb")

                    part = MIMEBase("application", "octet-stream")
                    part.set_payload((attachment).read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition", "attachment; filename= %s" % filename
                    )
                    msg.attach(part)
                    arquivoAnexo = True

        if arquivoAnexo or erro:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email, self.password)
            corpoEmail = msg.as_string()
            server.sendmail(self.email, destinatario, corpoEmail)
        
        server.quit()