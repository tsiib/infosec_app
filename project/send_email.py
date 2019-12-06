from flask import Flask, Blueprint
from flask_mail import Mail, Message
import os

send_email = Blueprint('send_email', __name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'bess.testin@gmail.com',
    "MAIL_PASSWORD": 'Bess.testin123'
}

send_email.config.update(mail_settings)
mail = Mail(send_email)
