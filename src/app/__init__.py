from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'registration.login'


from app.main.routes import main
from app.registration.routes import registration
from app.dictionary.routes import dictionary

app.register_blueprint(main)
app.register_blueprint(registration)
app.register_blueprint(dictionary)