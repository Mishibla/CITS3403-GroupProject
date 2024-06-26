from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'main.login'


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.config['STATIC_FOLDER'] = 'app/static'

    from app.blueprints import main
    app.register_blueprint(main)
    db.init_app(app)
    login.init_app(app)

    return app

from app import models







