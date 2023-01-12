# settings.py

import os

from flask_sqlalchemy import SQLAlchemy


APP_NAME = 'project.app'
DB_ORM = SQLAlchemy()
FLASK_ENV = os.getenv("FLASK_ENV")

if FLASK_ENV == "development":
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI_DEV",
    )
elif FLASK_ENV == "production":
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI_PROD")
else:
    raise RuntimeError(
        "Unexpected environement variable 'FLASK_ENV', "
        "expected values : 'production' or 'development', "
        f"got {str(FLASK_ENV)}"
    )
