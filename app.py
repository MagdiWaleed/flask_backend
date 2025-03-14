from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



db = SQLAlchemy()


def create_app():
    app = Flask(__name__,static_url_path='/profile_pics', static_folder='profile_pics')

    app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.db'

    app.secret_key = 'SOME KEY'
    app.config['UPLOAD_FOLDER'] = 'profile_pics'
    

    
    db.init_app(app)

    from routes import register_routes
    register_routes(app, db)

    #import later on

    migrage = Migrate(app,db)
    return app