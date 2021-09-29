import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from ml_api.models import db, Measure

load_dotenv()
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///measures.sqlite3"

db.init_app(APP)
#os.getenv('VARIABLE')

@APP.route('/hello')
def hello_world():
    return 'Hello, World!'

@APP.route('/sensor', methods=['GET', 'POST'])
def sensor():
    """
    Rota que recebe dados de frequência cardíaca e armazena no banco de dados.

    Converte o valor para um número que (caso fornecido) e faz a devidas validações.

    Retorna uma mensagem de erro específica em caso de falha.

    Arguments
    ----------
    medida (str): Valor que será armazenado.
    data: (str): Data em que a medição foi feita no formato '%d/%m/%Y:%H:%M:%S'.

    Returns
    ---------
    JSON (str): JSON com o resultado da operação.
    """
    route_params = ['medida', 'data']
    current_date = datetime.now().strftime("%d/%m/%Y:%H:%M:%S")
    measure_date = None
    
    result_object = {
        "result": None,
        "error": None,
        "timestamp": current_date 
    }

    if request.method == 'POST':
        for key in route_params:
            if not key in request.form:
                result_object["error"] = f"O valor '{key}' não foi fornecido."

        if not result_object["error"]:
            medida = request.form['medida']
            str_data = request.form['data']

            try:
                measure_date = datetime.strptime(str_data, "%d/%m/%Y:%H:%M:%S")
            except ValueError:
                error_ = "O Valor de 'data' não é valido."
                return { "result": None, "error": error_, "timestamp": current_date }


            if not medida.replace('.', '', 1).isdigit():
                result_object["error"] = "O Valor não é um número."
            else:
                measure = Measure(
                        medida=float(medida),
                        data=measure_date,
                        timestamp=datetime.now()
                )
                
                db.session.add(measure)
                db.session.commit()

                result_object["result"] = f"O valor {request.form['medida']}" \
                f" foi registrado."

        return json.dumps(
                result_object,
                sort_keys=True
            )
    else:
        return jsonify([
            dict(
                id=msr.id,
                medida=msr.medida,
                data=msr.data,
                timestamp=msr.timestamp
            ) for msr in Measure.query.all()
        ])
