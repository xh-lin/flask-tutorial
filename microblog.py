# The Flask Mega-Tutorial
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

from app import app, db
from app.models import User, Post

"""
(venv) $ flask shell
no longer needed to import by hand when debugging in shell
"""
@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Post': Post}