#!/usr/bin/python
from project.settings import DB_ORM
from project.app import app
DB_ORM.create_all(app=app)
