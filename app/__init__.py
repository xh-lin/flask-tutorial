from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
# configuration items can be accessed with a dictionary syntax from app.config
app.config.from_object(Config)

# initialize extensions:

db = SQLAlchemy(app) # database object
migrate = Migrate(app, db, render_as_batch=True) # migration engine
login = LoginManager(app)
login.login_view = 'login' # tell Flask-Login which view function handles logins

# enable the email logger when the application is running without debug mode
if not app.debug:
  # and also when the email server exists in the configuration (.flaskenv)
  if app.config['MAIL_SERVER']:
    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
      auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
      secure = ()
    mail_handler = SMTPHandler(
      mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
      fromaddr='no-reply@' + app.config['MAIL_SERVER'],
      toaddrs=app.config['ADMINS'], subject='Microblog Failure',
      credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # logging to a file
    if not os.path.exists('logs'):
      os.mkdir('logs')
    # RotatingFileHandler ensuring that the log files do not grow too large
    # limiting the size of the log file to 10KB, keeping the last ten log files as backup.
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # logging categories are DEBUG, INFO, WARNING, ERROR and CRITICAL in increasing
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
    
      
# import modules after the application instance is created
from app import routes, models, errors