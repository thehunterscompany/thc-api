from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from .utils.constants import *
from .utils.error_handler import error_handler

def setup_db(app, db_name=DATABASE_NAME):
    app.config['MONGODB_SETTINGS'] = {
        'db': db_name,
        'host': DATABASE_HOST,
        'port': DATABASE_PORT
    }

    db = MongoEngine()
    db.init_app(app)


def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)
    if testing:
        setup_db(app, db_name=TEST_DATABASE_NAME)
    else:
        setup_db(app)

    @app.route('/')
    def welcome():
        return jsonify('The Hunters Company')

    error_handler(app)

    from .controllers import auth, document

    app.register_blueprint(auth.bp)
    app.register_blueprint(document.bp)

    return app
