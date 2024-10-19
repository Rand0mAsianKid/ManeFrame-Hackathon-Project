from flask import flask


def create_app():
    app = Flask (__Name__)
    app.config['SECRET_KEY'] = 'error 404:team not found'

    return app