from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Measure(db.Model):
    """
    Classe que representa a tabela no banco de dados das medidas registradas.

    Parameter
    --------

    id (int): Id da medida (chave-primaria).
    medida (float): Valor registrado pelo sensor.
    data (str): Data em que a medicao foi feita no formato dd//mm//YYYY:HH:MM:SS. 
    timestamp (DateTime): Data em que o valor foi registrado na API. 
    """
    id = db.Column('id', db.Integer, primary_key=True)
    medida = db.Column('medida', db.Float)
    data = db.Column('data', db.DateTime)
    timestamp = db.Column('timestamp', db.DateTime)


