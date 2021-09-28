import os
import json
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///measures.sqlite3"

db = SQLAlchemy(APP)

#os.getenv('VARIABLE')

class Measure(db.Model):
    """
    Classe que representa a tabela no banco de dados das medidas registradas.

    Parameter
    --------

    id (int): Id da medida (chave-primaria).
    medida (float): Valor registrado pelo sensor.
    timestamp (DateTime): Data em que o valor foi registrado na API. 
    """
    id = db.Column('id', db.Integer, primary_key=True)
    medida = db.Column('medida', db.Float)
    timestamp = db.Column('timestamp', db.DateTime)

@APP.route('/hello')
def hello_world():
    return 'Hello, World!'

@APP.route('/sensor', methods=['POST'])
def sensor():
    """
    Rota que recebe dados de frequência cardíaca e armazena no banco de dados.

    Converte o valor para um número que (caso fornecido) e faz a devidas validações.

    Retorna uma mensagem de erro específica em caso de falha.

    Arguments
    ----------
    medida (str): Valor que será armazenado.

    Returns
    ---------
    JSON (str): JSON com o resultado da operação.
    """
     
    current_date = datetime.now().strftime("%d/%m/%Y:%H:%M:%S")
    result_object = {
        "result": None,
        "error": None,
        "timestamp": current_date 
    }

    if not 'medida' in request.form:
        result_object["error"] = "O valor 'medida' não foi fornecido."
    else:
        medida = request.form['medida']

        if not medida.replace('.', '', 1).isdigit():
            result_object["error"] = "O Valor não é um número."
        else:
            measure = Measure(medida=float(medida), timestamp=datetime.now())
            db.session.add(measure)
            db.session.commit()

            result_object["result"] = f"O valor {request.form['medida']}" \
            f" foi registrado."

    return json.dumps(
            result_object,
            sort_keys=True
        )
