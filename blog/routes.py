"""
base routes for app
"""
from typing import Union

from flask import render_template, redirect, url_for, Response, flash, request
from flask_login import login_user, current_user, logout_user, login_required

from blog import app, db, brp
from blog.forms import RegistrationForm, LoginForm, UpdateProfileForm
from blog.models import User


@app.route('/')
def home() -> str:
    """
    :return home page
    :rtype str
    """
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register() -> Union[Response, str]:
    """
    :returns register form page
    :rtype: str
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pass = brp.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pass)
        db.session.add(user)
        db.session.commit()
        flash('Your registration done. . .', category='success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    :return login form page
    :rtype: str
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and brp.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next', None)
            flash('you logged in successfully', 'success ')
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash('email or password are wrong', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you logged out successfully', 'success')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('account updated', 'info')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('profile.html', form=form)
