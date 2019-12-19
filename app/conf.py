import os

#creating base directory
basedir = os.path.abspath(os.path.dirname(__file__))


#configuring database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False


#flask_admin configuration
FLASK_ADMIN_SWATCH = 'cerulean'

#secret Key
SECRET_KEY = '40b4739103be318ada4a909e6e3ac1a5bd40a5da28db408a385789b32affaba0'

#mail sending configuration
MAIL_SERVER ='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'joshyjoy.dev@gmail.com'
MAIL_PASSWORD = 'joshy@joykl007'
MAIL_USE_TLS = False
MAIL_USE_SSL = True


#image uploading path
IMAGE_UPLOADS = os.path.join(basedir, 'static/uploads')