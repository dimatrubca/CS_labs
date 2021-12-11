import smtplib, ssl
import random, os
from dotenv import load_dotenv
from os.path import join, dirname


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def send_email(receiver_email):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ['sender']  
    password = os.environ['password']

    code = random.randint(10000, 120000)

    message = """\
    Subject: Email Verification

    Hello! Thank you for joining!

    TO confirm your accoutn enter the code: {}""".format(code)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return str(code)