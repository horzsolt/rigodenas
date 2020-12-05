import smtplib, ssl, os
from configparser import ConfigParser
from loghelper import logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

def send_html_mail(message):
    try:
        message = MIMEMultipart('alternative')
        message["Subject"] = "-= MUSIC DL =-"
        message["From"] = sender_email
        message["To"] = [sender_email]

        part_html = MIMEText(message, "html")

        message.attach(part_html)


        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            raw = base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')
            server.sendmail(
                sender_email, sender_email, raw
            )
    except Exception as ex:
        logger.error(ex, exc_info=True)
        raise Exception(ex)

def send_plaintext_mail(message):

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            newline = "\n"
            message = f"Subject: -= MUSIC DL =- {newline}To: {sender_email}{newline}From: {sender_email}{newline}{message}"
            server.login(sender_email, password)
            server.sendmail(sender_email, sender_email, message)
    except Exception as ex:
        logger.error(ex, exc_info=True)
        #raise Exception(ex)

config_object = ConfigParser()
config_object.read(os.path.dirname(os.path.realpath(__file__)) + "/config.ini")
config = config_object["CONFIG"]
smtp_server = "smtp.gmail.com"
port = 465
sender_email = config["SENDER_MAIL"]
password = config["SENDER_PWD"]
context = ssl.create_default_context()