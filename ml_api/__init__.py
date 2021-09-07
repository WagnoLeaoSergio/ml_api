import os
from flask import Flask

APP = Flask(__name__)


@APP.route('/')
def index():
    return '<h1>Index Page</h1>'


@APP.route('/hello')
def hello_world():
    return 'Hello, World!'
