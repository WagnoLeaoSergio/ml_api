import os
import json
import pickle
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_migrate import Migrate

from sklearn.ensemble import GradientBoostingRegressor

from ml_api.models import db, Measure

load_dotenv()
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///measures.sqlite3"
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(APP)

with APP.app_context():
    db.create_all()

migrate = Migrate(APP, db)
#os.getenv('VARIABLE')



@APP.route('/hello')
def hello_world():
    """
    Rota que retorna um texto escrito 'Hello, World!'
    """
    return 'Hello, World!'

@APP.route('/previsao/', methods=['POST'])
def bpm():
    """
    Versão do Gabriel que recebe os dados de frequencia cardiaca e retorna a previsão gerada pelo modelo.
    
    Parameters
    ---------
    request (JSON): Objeto com o dados do usuario para serem usados na previsão.
    
    - maximo (float)
    - minimo (float)
    - frequencia (float)
    - aumento_frequencia (float)

    Returns
    -------
    response (JSON): Objeto Json com o campo 'previsao' contendo o resultado gerado pelo modelo.
    """
    local_dir = os.path.dirname(__file__)
    mlModel_path = os.path.join(local_dir, "modelo.sav")
    boost = pickle.load(open(mlModel_path, "rb"))

    colunas = ['maximo', 'minimo', 'frequencia', 'aumento_frequencia']
    informacao = request.get_json()
    informacao_input = [informacao[col] for col in colunas]
    bpm_previsto = boost.predict([informacao_input])
    return jsonify(previsao=bpm_previsto[0].round(2))

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
    route_params = [
            "maximo",
            "minimo",
            "frequencia",
            "aumento_frequencia",
            "data"
    ]
    #route_params = ['medida', 'data']
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
            # maximo = request.form['maximo']
            # minimo = request.form['minimo']
            # frequencia= request.form['frequencia']
            # aumento_frequencia = request.form['aumento_frequencia']
            str_data = request.form['data']
            try:
                measure_date = datetime.strptime(str_data, "%d/%m/%Y:%H:%M:%S")
            except ValueError:
                error_ = "O Valor de 'data' não é valido."
                return { "result": None, "error": error_, "timestamp": current_date }

            params = ['maximo', 'minimo', 'frequencia', 'aumento_frequencia']

            for param in params:
                if not request.form[param].replace('.', '', 1).isdigit():
                    result_object["error"] = "O Valor não é um número."
            else:
                #: Carrega o modelo
                local_dir = os.path.dirname(__file__)
                mlModel_path = os.path.join(local_dir, "modelo.sav")
                boostModel =  pickle.load(open(mlModel_path, "rb"))
                
                #: Faz a previsão
                informacao_input = [request.form[col] for col in params]
                bpm_previsto = boostModel.predict([informacao_input])

                #: Salva os dados no banco
                measure = Measure(
                        maximo=float(request.form['maximo']),
                        minimo=float(request.form['minimo']),
                        frequencia=float(request.form['frequencia']),
                        aumento_frequencia=float(request.form['aumento_frequencia']),
                        previsao=float(bpm_previsto[0].round(2)),
                        data=measure_date,
                        timestamp=datetime.now()
                )
                
                db.session.add(measure)
                db.session.commit()
                
                result_object["previsao"] = bpm_previsto[0].round(2)
                result_object["result"] = f"Valores armazenados com sucesso."

        return json.dumps(
                result_object,
                sort_keys=True
            )
    else:
        return jsonify([
            dict(
                id=msr.id,
                data=msr.data,
                timestamp=msr.timestamp,
                maximo=msr.maximo,
                minimo=msr.minimo,
                frequencia=msr.frequencia,
                aumento_frequencia=msr.aumento_frequencia,
                previsao=msr.previsao
            ) for msr in Measure.query.all()
        ])
