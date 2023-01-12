from flask_login import UserMixin
from project.settings import DB_ORM as db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(20))
