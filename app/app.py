import os
from flask.cli import FlaskGroup

from app import create_app, db


config_name = os.getenv('FLASK_CONFIG', 'default')
app = create_app(config_name)
cli = FlaskGroup(create_app=create_app)


if __name__ == "__main__":
    cli()
