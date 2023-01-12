# auth.py

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import Forbidden
from project.settings import DB_ORM, FLASK_ENV
import os

from project.models.auth import User

auth = Blueprint('auth', __name__)

RETRY_MESSAGE = 'Please check your login details and try again.'
EXISTING_USER_MESSAGE = 'A user with that email already exists.'
NOT_IMPLEMENTED_ERROR_MESSAGE = "Route not implemented in production"


@auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(name=name).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        logout_user()
        return Response(
            "Are you sure you're part of the club ?",
            status=400,
        )

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.index'))


@auth.route('/admin_login', methods=['POST'])
def login_admin():
    name = os.getenv("ADMIN_USER_NAME")
    password = request.form.get('password')

    user = User.query.filter_by(name=name).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        logout_user()
        return Response(
            "You tryin to fool me you fool ?",
            status=400,
        )

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.admin'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
