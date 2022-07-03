# syntax=docker/dockerfile:1

FROM python:3.6.15-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=ml_api
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
