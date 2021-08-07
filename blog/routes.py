"""
base routes for app
"""
from typing import Union

from flask import render_template, redirect, url_for, Response, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from blog import app, db, brp
from blog.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm
from blog.models import User, Post


@app.route('/')
def home() -> str:
    """
    :return home page
    :rtype str
    """
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route('/post/<int:post_id>')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail.html', post=post)


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


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('post created', 'info')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form)


@app.route('/post/<int:post_id>/delete')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post deleted', 'info')
    return redirect(url_for('home'))


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('post updated', 'info')
        return redirect(url_for('detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update.html', form=form)
