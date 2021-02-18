import datetime

from flask import current_app
from flask_mail import Mail, Message

from app.utils.constants import *


def setup_email(app):
    """
    Setup config variables
    :param app: flask app
    """
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT


def send_mail(recipient, html, subject):
    mail = Mail(current_app)
    msg = Message(subject, sender='ajzpiv97@gmail.com', recipients=[recipient], html=html)
    mail.send(msg)
