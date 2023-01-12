# main.py

import os
import logging
import PIL.Image
import math
from flask import Blueprint, Response, render_template, request, redirect, url_for, jsonify
from flask_login import current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from project.settings import (
    APP_NAME,
    DB_ORM,
)
from flask import current_app as app
from project.models.auth import User
from project.models.image import Image

main = Blueprint('main', __name__)
logger = logging.getLogger(APP_NAME)
ALLOWED_COLORS = {'all', '000000', 'FFE800', '46AF0E', '006872', '0048BC', 'FF6CE3', 'ED322E'}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    return redirect(url_for('main.show_images', color="all"))


# FULL SCREEN IMAGE
@main.route('/<int:image_id>', methods=['GET'])
def get_image_full_screen(image_id):
    image = Image.query.get_or_404(image_id)
    image_to_display = f"{app.config['UPLOAD_FOLDER']}{image.name}"
    return render_template('image.html', image=image_to_display, infos=image)


@main.route('/color/<color>', methods=['GET'])
def show_images(color):
    if color not in ALLOWED_COLORS:
        return Response(
            "Watch out you fool",
            status=400,
        )

    # CREATE BASIC USER IF NOT EXISTING :
    basic_user = User.query.filter_by(name=os.getenv("BASIC_USER_NAME")).first()
    if basic_user is None:
        # create super user
        basic_user = User(
            name=os.getenv("BASIC_USER_NAME"),
            password=generate_password_hash(
                os.getenv("BASIC_USER_PASSWORD"),
                method='sha256'
            ),
        )
        DB_ORM.session.add(basic_user)
        DB_ORM.session.commit()

    # CREATE ADMIN USER IF NOT EXISTING :
    admin_user = User.query.filter_by(name=os.getenv("ADMIN_USER_NAME")).first()
    if admin_user is None:
        # create super user
        admin_user = User(
            name=os.getenv("ADMIN_USER_NAME"),
            password=generate_password_hash(
                os.getenv("ADMIN_USER_PASSWORD"),
                method='sha256'
            ),
        )
        DB_ORM.session.add(admin_user)
        DB_ORM.session.commit()

    # FETCH IMAGES FROM DB
    files_list = []
    # FILTER
    if color == "all":
        # ALL QUERY
        files = (
            Image.query
            .filter(Image.accepted == True)  # noqa
            .order_by(Image.id.asc())
        )
    else:
        # COLOR SPECIFIC QUERY
        files = (
            Image.query
            .filter_by(color=color)
            .filter(Image.accepted == True)  # noqa
            .order_by(Image.id.asc())
        )

    for file in files:
        image_from_db = {
            "id": file.id,
            "file": f"../{app.config['UPLOAD_FOLDER']}compressed_images/{file.name}",
            "color": f"#{file.color}",
            "details": file.details
        }
        files_list.append(image_from_db)

    # GROUP IMAGE BY PACK OF 7 FOR FRONTEND
    files_list = [files_list[n:n + 7] for n in range(0, len(files_list), 7)]

    return render_template('index.html', files=files_list)


def minimize_file(file_path, thumbnail=False):
    quality = 35 if thumbnail else 65
    max_size = 1055000 if thumbnail else 20000000
    ratio_division = 2 if thumbnail else 1.5

    size = os.path.getsize(file_path)
    image = PIL.Image.open(file_path)

    while size > max_size:
        width, height = image.size
        width, height = math.floor(width / ratio_division), math.floor(height / ratio_division)
        image = image.resize((width, height), PIL.Image.ANTIALIAS)
        image.save(file_path, optimize=True, quality=quality)
        image = PIL.Image.open(file_path)
        size = os.path.getsize(file_path)
    return image


# SINGLE FILE UPLOAD
@ main.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return Response(
                "No files in request",
                status=400,
            )
        files = request.files.getlist('files[]')
        file = files[0]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # SET PATH TO UPLOAD DIRECTORY
            uploads_dir = f"{os.getcwd()}/project/{app.config['UPLOAD_FOLDER']}"

            # CHECK DB IF FILE ALREADY EXIST
            already_in_db = Image.query.filter_by(name=filename).first()

            if already_in_db is None:

                # SAVE PRETTY FILE
                file_path = os.path.join(uploads_dir, filename)
                file.save(file_path)
                image = minimize_file(file_path, thumbnail=False)

                # MAKE THUMBNAIL
                thumbnail_path = f"{uploads_dir}/compressed_images/{filename}"
                image.save(thumbnail_path, optimize=True, quality=30)
                minimize_file(thumbnail_path, thumbnail=True)

                # GET DIMENSION OF FILE FOR DB
                image = PIL.Image.open(thumbnail_path)
                width, height = image.size
                image_size = f"{width}x{height}"

                # ADD IMAGE TO DB
                new_image = Image(
                    name=filename,
                    color=request.form.get('color'),
                    details={
                        "size": image_size,
                        "insta": request.form.get('insta'),
                        "artist_name": request.form.get('artist_name'),
                        "email": request.form.get('artist_email')
                    }
                )
                DB_ORM.session.add(new_image)
                DB_ORM.session.commit()
                return Response(
                    "Image uploaded.",
                    status=200,
                )
            else:
                return Response(
                    "Image is already uploaded.",
                    status=400,
                )
        else:
            return Response(
                "Allowed image types are -> png, jpg, jpeg, gif",
                status=400,
            )


# ADMIN SPACE
@main.route('/admin', methods=['GET'])
def admin_login():
    return render_template('admin.html')


@main.route('/admin/home', methods=['GET'])
def admin():
    try:
        name = current_user.name
    except AttributeError as e:
        return redirect(url_for('main.index'))

    if name != os.getenv("ADMIN_USER_NAME"):
        return Response(
            "Stop tryin to hack me pls",
            status=400,
        )

    files_list = []
    files = (
        Image.query
        .filter(Image.accepted == False)  # noqa
        .order_by(Image.id.asc())
    )

    for file in files:
        image_from_db = {
            "id": file.id,
            "file": f"../{app.config['UPLOAD_FOLDER']}compressed_images/{file.name}",
            "color": f"#{file.color}",
            "details": file.details
        }
        files_list.append(image_from_db)

    return render_template('admin_home.html', files=files_list)


# ACCEPT OR DELETE FILE :
@main.route('/image/<int:image_id>', methods=['POST', 'DELETE'])
def accept_or_delete_file(image_id):
    if request.method == 'POST':
        image = Image.query.get_or_404(image_id)
        image.accepted = True
        DB_ORM.session.commit()
        return Response(
            "ACCEPTED",
            status=200,
        )
    elif request.method == 'DELETE':
        image = Image.query.get_or_404(image_id)
        uploads_dir = f"{os.getcwd()}/project/{app.config['UPLOAD_FOLDER']}"
        raw_file = f"{uploads_dir}/{image.name}"
        compressed_file = f"{uploads_dir}/compressed_images/{image.name}"

        try:
            os.remove(raw_file)
            os.remove(compressed_file)
        except OSError as e:
            return f"Error: {e.filename} - {e.strerror}."

        DB_ORM.session.delete(image)
        DB_ORM.session.commit()
        return Response(
            "DELETED",
            status=200,
        )
