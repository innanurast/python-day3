FROM python:3.10.10-bullseye

RUN apt update
RUN apt install python3-pip -y

RUN pip3 install flask==2.0.2 werkzeug==2.0.2
RUN pip3 install python-decouple==3.6 python-dotenv==0.20.0
RUN pip3 install flask-restx==0.5.1
RUN pip3 install Flask-Migrate==3.1.0 Flask-SQLAlchemy==2.5.1 PyMySQL==1.0.2 SQLAlchemy==1.4.30

WORKDIR /trainapi

COPY . .

CMD flask run