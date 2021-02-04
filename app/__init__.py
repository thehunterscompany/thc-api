from flask import Flask, jsonify, request, abort
from flask_mongoengine import MongoEngine
from mongoengine.errors import NotUniqueError

from .collections.role import Roles
from .utils.contants import *


def create_app():
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'db': DATABASE_NAME,
        'host': DATABASE_HOST,
        'port': DATABASE_PORT
    }

    db = MongoEngine()
    db.init_app(app)

    @app.route('/')
    def welcome():
        return jsonify('The Hunters Company')

    # Endpoint
    @app.route('/roles', methods=['POST'])
    def post_roles():
        role_type = request.form['type']
        description = request.form['description']
        role = Roles(type=role_type, description=description)
        try:
            role.save()
        except NotUniqueError:
            abort(422)

        return jsonify({'success': True, 'result': role.format()})

    # Error Handling
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'result': {
            'success': False,
            "error": 404,
            "message": "not found"
        }}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'result': {
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }}), 422

    from .controllers import auth

    app.register_blueprint(auth.bp)

    return app
