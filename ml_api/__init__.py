import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from ml_api.models import db, Measure, User

from ml_api.routes.sensor import sensor
from ml_api.routes.gfit import gfit

load_dotenv()
APP = Flask(__name__)

APP.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
APP.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
APP.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db.init_app(APP)

with APP.app_context():
    db.create_all()

migrate = Migrate(APP, db)

APP.register_blueprint(sensor)
APP.register_blueprint(gfit)

ADMIN = Admin(APP, name='ml_api', template_mode='bootstrap3')

ADMIN.add_view(ModelView(Measure, db.session))
ADMIN.add_view(ModelView(User, db.session))

if __name__ == '__main__':
    APP.run()
