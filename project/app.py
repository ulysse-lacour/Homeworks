import logging
import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from project.auth import auth as auth_blueprint
from project.main import main as main_blueprint
from project.models.auth import User
from project.settings import DB_ORM, FLASK_ENV, SQLALCHEMY_DATABASE_URI


def initialize_db(app: Flask) -> None:
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    DB_ORM.init_app(app)


def initialize_app(testing: bool = False) -> Flask:

    app = Flask(__name__)
    # Setting logger level
    if FLASK_ENV == "development":
        app.logger.setLevel(level=logging.INFO)
    else:
        app.logger.setLevel(level=logging.DEBUG)

    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if not testing:
        initialize_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: int):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.filter_by(id=user_id).first()

    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    app.register_blueprint(main_blueprint)

    # set up for files upload
    UPLOAD_FOLDER = 'static/uploads/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 5000000

    return app


app = initialize_app()
migrate = Migrate(app=app, db=DB_ORM)
