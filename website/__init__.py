from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from flask_uploads import UploadSet, IMAGES, configure_uploads
from os import path
from flask_login import LoginManager
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField

# photos = UploadSet('profile_pic', IMAGES) 
class UploadProfile(FlaskForm):
    profile_pic = FileField('profile_pic')
    submit = SubmitField("Upload Profile Picture")


db = SQLAlchemy()
ma = Marshmallow()
DB_NAME = "database.db"
IMAGE_FOLDER = 'static/images'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key'
    app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.route('/' + IMAGE_FOLDER + '/<filename>')
    def get_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
