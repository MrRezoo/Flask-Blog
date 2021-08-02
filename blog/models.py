"""
 Build models
"""
from flask_login import UserMixin
from sqlalchemy.sql.functions import now

from blog import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        """
        :return: show instance for developers
        """
        return f'{self.__class__.__name__}({self.id}, {self.username})'


class Post(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    title = db.Column(db.String(120), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=now)
    content = db.Column(db.TEXT, nullable=False)

    def __repr__(self):
        """
              :return: show instance for developers
              """
        return f"{self.__class__.__name__}({self.id}, {self.title[:30]}, {self.date})"
