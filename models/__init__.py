from flask_sqlalchemy import SQLAlchemy

# Tworzenie obiektu bazy danych
db = SQLAlchemy()

# Importowanie modeli
from .user import User
from .task import Task

# Inicjowanie bazy danych
def init_db():
    db.create_all()