from flask import Flask, render_template, redirect, url_for, flash, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,  login_user, login_required, logout_user, current_user
from auth.forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_bootstrap import Bootstrap
from config import start, loginManeger
from auth.authController import auth
from tasks.taskController import tasks
from models import db, User, Task

app = Flask(__name__)
start(app=app, db = db)
login_manager = loginManeger(app)

app.register_blueprint(auth)
app.register_blueprint(tasks)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def start():
   return redirect(url_for('auth.login'))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Nie znaleziono'}),404)

@app.route('/this_route_does_not_exist')
def get_nonexistent_route():
    pass

@app.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': 'Brak dostępu'}),403)

@app.route('/forbidden')
def get_forbidden():
    pass


def create_default_user():
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('admin', method='pbkdf2')
        admin = User(username='admin',email = 'admin@admin.pl' ,role='admin', password_hash = hashed_password)
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_default_user()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)