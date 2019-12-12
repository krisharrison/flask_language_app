from flask import Blueprint, render_template
from app.models import Dictionary

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    words = Dictionary.query.all()
    return render_template('home.html', title = 'Dictionary', words = words)

@main.route('/about')
def about():
    return render_template('about.html')