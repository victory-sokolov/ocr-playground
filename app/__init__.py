import os
from pathlib import Path

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

from app.config import config

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_name) -> object:
    app = Flask(__name__, template_folder="templates")

    if not isinstance(config_name, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    CORS(app)

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # shell context for flask cli

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
