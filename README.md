
## Dependências:

- python ^3.6
- Flask 1.1.2

## Como configurar o projeto

Primeiramente inicie um ambiente virtual usando a biblioteca `virtualenv`:

```bash
virtualenv .venv
. .venv/bin/activate
```

Com o terminal na pasta do projeto, execute as seguintes linhas de código:

```bash
pip install -r requirements.txt
```

## Como executar o projeto

Exporte as variáveis de ambiente através dos comandos:

```bash
export FLASK_APP=ml_api
export FLASK_ENV=development
```
Em seguida execute o comando abaixo para iniciar o serviço:

```bash
flask run
```

## Como criar uma image Docker do projeto

O Dockerfile do projeto já está incluso, para a criação da sua imagem basta executar o comando:

```bash
docker build --tag ml_api .
```

Com a imagem da API criada, basta executar o comando:

```bash
docker run ml_api
```
