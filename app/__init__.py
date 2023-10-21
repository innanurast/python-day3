from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .config.config import config_dict
from .views.users import users_ns
from .views.auth import auth_ns
from .utils import db
# from flask_sqlalchemy import SQLAlchemy
from .models import users
from .logs.log import flasklogger

def create_app(config=config_dict['dev']):


    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    api = Api(
        app,
        doc='/docs',
        title="REST API FLASK",
        description="Latihan Membuat REST API dengan Flask",
        authorizations= {
            "Bearer Auth" : {
                "type": 'apiKey',
                "in": 'header',
                "name": 'Authorization',
                "description": 'jwt api'
            }
        },
        security= "Bearer Auth"
    )

    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)

    migrate = Migrate(app, db)

    jwt = JWTManager(app)

    flasklogger.debug('Initial run API flask')

    return app