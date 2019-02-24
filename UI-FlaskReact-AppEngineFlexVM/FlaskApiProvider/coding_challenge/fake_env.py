import json
import os

from flask_mail import Message, Mail
from flask import current_app as app

datastore_client = None
bigquery_client = None
storage_client = None

MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'

try:
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
except ValueError:
    #input wasn't an int
    raise ValueError('MAIL_PORT must be an integer')
except TypeError:
    #no input provided, use default gmail port
    MAIL_PORT = 465

MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
MAIL_SUPPRESS_SEND = bool(os.environ.get('FAKE_EMAIL')) or False

def get_email_client():
    app.config.update(dict(
        MAIL_SERVER = MAIL_SERVER,
        MAIL_PORT = MAIL_PORT,
        MAIL_USE_TLS = MAIL_USE_TLS,
        MAIL_USE_SSL = MAIL_USE_SSL,
        MAIL_USERNAME = MAIL_USERNAME,
        MAIL_PASSWORD = MAIL_PASSWORD,
        MAIL_DEFAULT_SENDER = MAIL_USERNAME,
        MAIL_SUPPRESS_SEND = MAIL_SUPPRESS_SEND
    ))
    mail = Mail()
    mail.init_app(app)
    return mail
