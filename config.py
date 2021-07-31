# similar to global variables

import os
# main directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
  # tell Flask-SQLAlchemy extension where to put the database file
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
  # Do not signal the application every time a change is about to be made in the database
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  """
  email server details:
  include the server and port, 
  a boolean flag to enable encrypted connections, 
  and optional username and password
  """
  # os.environ variables see file .flaskenv
  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  ADMINS = ['admin@example.com']

  POSTS_PER_PAGE = 3