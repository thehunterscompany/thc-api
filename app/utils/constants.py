import os

DATABASE_NAME = os.getenv('DATABASE_NAME', 'thc')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME', 'thc_test')
DATABASE_PORT = int(os.getenv('DATABASE_PORT', 27017))

MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 465))
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
MAIL_USE_SSL = bool(os.getenv('MAIL_USE_SSL', True))

SECRET_KEY = os.getenv('SECRET_KEY', '')
SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', '')
