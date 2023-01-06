from flask import Flask
from os import path
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# init flask app
app = Flask(__name__)
db = SQLAlchemy()

# function starter
def create_app():
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    # routes imported
    from .views import views
    from .auth import auth

    # register our routes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # import models to create the db table
    from .models import User, Note

    database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
    
def database(app):
    if not path.exists('website/database.db'):
        with app.app_context():
            db.create_all()
            print('Database Created Successfully!')

