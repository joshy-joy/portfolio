import os

#creating base directory
basedir = os.path.abspath(os.path.dirname(__file__))


#configuring database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') #'sqlite:///' + os.path.join(basedir, 'db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False


#flask_admin configuration
FLASK_ADMIN_SWATCH = 'cerulean'

#secret Key
SECRET_KEY = os.environ.get('SECRET_KEY')

#mail sending configuration
MAIL_SERVER ='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USE_TLS = False
MAIL_USE_SSL = True

#AWS S3 configurations
S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

