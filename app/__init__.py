from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from .utils.contants import *

def create_app():
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'db': DATABASE_NAME,
        'host': DATABASE_HOST,
        'port': DATABASE_PORT
    }

    MongoEngine(app)
    # db = MongoEngine(app)
    # db.init_app(app)

    @app.route('/')
    def welcome():
        return jsonify('The Hunters Company')

    @app.errorhandler(404)
    def page_not_found(error):
        return { 'result': 'not_found' }, 404

    from .controllers import auth

    app.register_blueprint(auth.bp)

    return app
