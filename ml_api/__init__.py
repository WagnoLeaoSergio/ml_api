import os
import json
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
APP = Flask(__name__)

#os.getenv('VARIABLE')

@APP.route('/')
def index():
    return '<h1>Index Page</h1>'


@APP.route('/hello')
def hello_world():
    return 'Hello, World!'

@APP.route('/sensor', methods=['POST'])
def sensor():
    return json.dumps({
        "result": f"O valor {request.form['measure']} foi registrado"    
    })
