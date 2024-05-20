from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import *

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://DB_USER:DB_PASS@DB_HOST/DB_NAME'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    from .models import Paciente

    @login_manager.user_loader
    def load_user(user_id):
        return models.query.get(int(user_id))

    # Register blueprints
    from .hello_run import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .hello_run import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
