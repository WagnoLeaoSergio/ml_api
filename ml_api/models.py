from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    Classe que representa a tabela no banco de dados dos usuários registrados no sistema.

    Parameters
    ----------
    id (int): Id do usuario (chave-primaria).
    apelido (str): apelido do usuario no sistema.
    """
    id = db.Column('id', db.Integer, primary_key=True)
    apelido = db.Column('apelido', db.String(80), unique=True, nullable=False)

class Measure(db.Model):
    """
    Classe que representa a tabela no banco de dados das medidas registradas.

    Parameters
    --------

    id (int): Id da medida (chave-primaria).
    medida (float): Valor registrado pelo sensor.
    data (str): Data em que a medicao foi feita no formato dd//mm//YYYY:HH:MM:SS. 
    timestamp (DateTime): Data em que o valor foi registrado na API. 
    """
    id = db.Column('id', db.Integer, primary_key=True)
    maximo = db.Column('maximo', db.Float)
    minimo = db.Column('minimo', db.Float)
    frequencia = db.Column('frequencia', db.Float)
    aumento_frequencia = db.Column('aumento_frequencia', db.Float)
    previsao = db.Column('previsao', db.Float)
    data = db.Column('data', db.DateTime)
    timestamp = db.Column('timestamp', db.DateTime)
