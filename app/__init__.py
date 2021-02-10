from flask import Flask, jsonify
from mongoengine import connect
from .utils.constants import *
from .utils.error_handler import error_handler

def setup_db(db_name=DATABASE_NAME):
    connect(db_name, host=DATABASE_HOST, port=DATABASE_PORT)

def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)
    if testing:
        setup_db(db_name=TEST_DATABASE_NAME)
    else:
        setup_db()

    @app.route('/')
    def welcome():
        return jsonify('The Hunters Company')

    error_handler(app)

    from .controllers import auth, document, role, client_type

    app.register_blueprint(auth.bp)
    app.register_blueprint(document.bp)
    app.register_blueprint(role.bp)
    app.register_blueprint(client_type.bp)

    return app
