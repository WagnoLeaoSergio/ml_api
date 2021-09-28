import os
import json
from datetime import datetime
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
    """
    Rota que recebe um valor do sensor de frequência cardíaca e armazena no banco de dados.

    Arguments
    ----------
    measure (int, float): - Valor que será armazenado.

    Returns
    ---------
    JSON (str): JSON com o resultado da operação.
    """
    measure = request.form['measure']
    current_date = datetime.now().strftime("%d/%m/%Y:%H:%M:%S")
    
    result_object = {
        "result": None,
        "error": None,
        "timestamp": current_date 
    }

    if not measure.replace('.', '', 1).isdigit():
        result_object["error"] = "O Valor não é um número."
    else:
        result_object["result"] = f"O valor {request.form['measure']}" \
        f" foi registrado na data {current_date}."

    return json.dumps(
            result_object,
            sort_keys=True
        )
