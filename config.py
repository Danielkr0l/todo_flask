from flask_login import LoginManager
def start(app, db):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'Qazwsxedcrfvtgb' 
    db.init_app(app)

def loginManeger(app):
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    return login_manager