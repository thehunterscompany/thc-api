from flask import Flask, jsonify
from flask_mongoengine import MongoEngine

from .utils.contants import *


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

    # Error Handling
    @app.errorhandler(400)
    def page_not_found(e):
        return jsonify({'result': "bad request",
                        }), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'result': "not found",
                        }), 404

    @app.errorhandler(405)
    def unprocessable(e):
        return jsonify({'result': "method not allowed"
                        }), 405

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({'result': "unprocessable"
                        }), 422

    from .controllers import auth

    app.register_blueprint(auth.bp)

    return app
