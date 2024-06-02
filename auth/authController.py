from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,  login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User
from flask import Blueprint
from functools import wraps

auth = Blueprint('auth', __name__)




@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            if user.role == 'admin':
                return redirect(url_for('tasks.everyTask'))
            return redirect(url_for('tasks.allTasks'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2')
        new_user = User(email = form.email.data,username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return func(*args, **kwargs)
        return decorated_view
    return decorator

