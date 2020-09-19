import os

from flask import jsonify, render_template, request
from flask.cli import FlaskGroup

from app import create_app, db

config_name = os.getenv('FLASK_CONFIG', 'default')
app = create_app(config_name)
cli = FlaskGroup(create_app=create_app)


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=["POST"])
def upload_image():
    file = request.files['file']
    return jsonify({'status': 'Image recevied'}), 200


if __name__ == "__main__":
    cli()
