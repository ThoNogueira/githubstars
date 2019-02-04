import os
import logging

from flask_compress import Compress

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'storage.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Define uma chave secreta que será utilizada pelo FLASK. Para produção seria ideal registrá-la no SO do servidor.
    SECRET_KEY = '03b232a9a2342055e12028a2681c7532'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_LOCATION = 'githugstars.log'
    LOGGING_LEVEL = logging.DEBUG
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml',
                          'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    # Desativa a ordenação de chaves no json.
    JSON_SORT_KEYS = False


def configure_app(app):
    app.config.from_object(BaseConfig)
    # Configura o logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    # Configura Compressing
    Compress(app)