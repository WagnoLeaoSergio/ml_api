
##Dependências:

python 3.6^
Flask 1.1.2

##Como consfigurar o projeto

Com o terminal na pasta do projeto, execute as seguintes linhas de código:

pip install -r requirements.txt

##Como rodar o projeto

Exporte as variáveis de ambiente através dos comandos:

export FLASK_APP=flaskr
export FLASK_ENV=development

##Como criar a sua imagem do Docker

O Dockerfile do projeto já está incluso, para a criação da sua imagem basta executar o comando:

docker build --tag flaskr .
