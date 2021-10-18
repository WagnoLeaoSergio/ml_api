import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from ml_api.models import db

from ml_api.routes.sensor import sensor

load_dotenv()
APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
APP.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

db.init_app(APP)

with APP.app_context():
    db.create_all()

migrate = Migrate(APP, db)

APP.register_blueprint(sensor)
