from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt




db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.db'

    app.secret_key = 'SOME KEY'

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    bcrypt = Bcrypt(app)

    db.init_app(app)

    from routes import register_routes
    register_routes(app, db, bcrypt)

    #import later on

    migrage = Migrate(app,db)
    return app