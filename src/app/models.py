from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique=True) 
    password = db.Column(db.String(60), nullable=False)

    dictionary= db.relationship('Dictionary', backref='word', lazy=True)
    flash_cards = db.relationship('Flash_Cards', backref='score', lazy=True)


class Dictionary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english_word = db.Column(db.String(20), nullable=False, unique=True)
    german_article = db.Column(db.String(), default='N/A')
    german_word = db.Column(db.String(20), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Flash_Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_score = db.Column(db.Integer, nullable=False)
    last_loggedin = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)