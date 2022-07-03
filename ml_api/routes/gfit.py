import os
import json
import pickle
import requests
from datetime import datetime
from requests.structures import CaseInsensitiveDict
from flask import request, jsonify, Blueprint, current_app
from werkzeug.utils import secure_filename
from ml_api.models import db, Measure, User

gfit = Blueprint('gfit', __name__, url_prefix='/gfit')

@gfit.route('/')
def get_steps_data():
    """
    Rota que retorna um texto escrito 'Hello, World!'
    """

    query = request.args.to_dict()

    if 'email' not in query:
        return jsonify({
            "error": "email do usuario não especificado"        
        })


    auth_service_url = "http://localhost:3001/users"

    response = requests.get(auth_service_url)

    if response.status_code == 200:
        response_data = list(response.json())

        access_token = [ user for user in response_data if user['email'] == query['email'] ]
        if not len(access_token):
            return jsonify({
                "error": "Usuário especificado não encontrado"        
            })

        token = access_token[0]['access_token']
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = f"Bearer {token}"

        gfit_steps_url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        
        data_parameters = {
            "aggregateBy": [
                {
                    "dataTypeName": "com.google.step_count.delta",
                    "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
                }
            ],
            "startTimeMillis": int(datetime.now().timestamp() * 1000 - 7 * 86400000),
            "endTimeMillis": int(datetime.now().timestamp() * 1000)
        }

        gfit_response = requests.post(gfit_steps_url, json=data_parameters, headers=headers)

        if gfit_response.status_code == 200:
            return jsonify(gfit_response.json())
        else:
            print(gfit_response.json())
            return jsonify({
                "error": "Falha ao acessar serviços do Google Fit"        
            })
    else:
        return jsonify({
            "error": "Falha ao fazer requisição para o serviço de autentificação"        
        })

