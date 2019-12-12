from flask import Blueprint, render_template, flash, url_for, redirect, request
from app.registration.forms import Registration, Login, Account
from app import bcrypt, db
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required



registration = Blueprint('registration', __name__)

@registration.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        redirect(url_for('main.home'))

    form = Registration()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'Success')  
        return redirect(url_for('registration.login'))
    return render_template('register.html',title = 'Register', form = form)

@registration.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('main.home'))

    form = Login()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page= request.args.get('next', 'home')
            return redirect(next_page)
        else:
            flash('Error: wrong username or password', 'warning')
    return render_template('login.html', title = 'Login', form = form)


@registration.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@registration.route('/account', methods=[ 'GET','POST'])
@login_required
def account():
    form = Account()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('registration.account'))
        flash('Your account has been updated', 'message')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form = form)
