from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../blog.db'
app.config['SECRET_KEY'] = '0fcd57c66ef32208bf531bf7b6717525859fe1224cea9bfe57d39e13cae48ebe'
db = SQLAlchemy(app)
brp = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from blog import routes  # circular import error
