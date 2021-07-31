"""
following are models stored in the database
need to generate a database migration every time the database is modified:
(venv) $ flask db migrate -m "new fields in x model"
(venv) $ flask db upgrade
"""

from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

"""       followers
follower_id     INTEGER
followed_id     INTEGER
"""
# Followers association table
followers = db.Table('followers',
  db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# VARCHAR (n) is a string of max length n
"""       users
id              INTEGER
username        VARCHAR (64)
email           VARCHAR (120)
password_hash   VARCHAR (128)
"""
""" Example:
>>> u = User(username='john', email='john@example.com')
>>> db.session.add(u)
>>> db.session.commit()
"""
class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True, nullable=False)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  # one-to-many relationship (one)
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  # many-to-many relationship
  # the left side user is following the right side user (follower, followed)
  followed = db.relationship(
    'User', secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    #  "identicon" returns a geometric design that is different for every email
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
      digest, size)

  def __repr__(self):
    return '<User {}>'.format(self.username)

  def follow(self, user):
    if not self.is_following(user):
      self.followed.append(user)

  def unfollow(self, user):
    if self.is_following(user):
      self.followed.remove(user)

  def is_following(self, user):
    # look for items in the association table that have 
    # the left side foreign key set to the self user, 
    # and the right side set to the user argument
    # count() will return 1 or 0
    return self.followed.filter(
      followers.c.followed_id == user.id).count() > 0

  def followed_posts(self):
    # create a temporary table combines posts and followers tables, id matched
    followed = Post.query.join(
      followers, (followers.c.followed_id == Post.user_id)
      ).filter(followers.c.follower_id == self.id)
    own = Post.query.filter_by(user_id=self.id)
    return followed.union(own).order_by(Post.timestamp.desc())
    


"""       posts
id              INTEGER
body            VARCHAR (140)
timestamp       DATETIME
user_id         INTEGER
"""
""" Example:
>>> u = User.query.get(1)
>>> p = Post(body='my first post!', author=u)
>>> db.session.add(p)
>>> db.session.commit()
"""
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  # one-to-many relationship (many)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Post {}>'.format(self.body)


# allow Flask-Login to load users
@login.user_loader
def load_user(id):
  return User.query.get(int(id))