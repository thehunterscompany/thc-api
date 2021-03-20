from flask import Flask, jsonify
from flask_cors import CORS
from mongoengine import connect, NULLIFY, CASCADE
from .collections.client import Clients
from .collections.credit_line import CreditLines
from .collections.profile import Profiles
from .utils.config.email import setup_email
from .utils.constants import *
from .utils.error_handler import error_handler
from .middlewares import ContentTypeMiddleware
from .utils.setup_logger import init_logger


def setup_db(db_name=DATABASE_NAME):
    connect(db_name, host=DATABASE_HOST, port=DATABASE_PORT)


def create_app(testing=False):
    init_logger()
    app = Flask(__name__, instance_relative_config=True)

    setup_email(app)

    if testing:
        app.config['TESTING'] = True
        setup_db(db_name=TEST_DATABASE_NAME)
    else:
        setup_db()

    CORS(app, resources={r"/*": {"origins": "*"}},
         supports_credentials=True
         )

    @app.after_request
    def add_headers(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response

    @app.route('/')
    def welcome():
        return jsonify('The Hunters Company')

    error_handler(app)

    from .controllers import auth, document, role, client_type

    app.wsgi_app = ContentTypeMiddleware(app.wsgi_app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(document.bp)
    app.register_blueprint(role.bp)
    app.register_blueprint(client_type.bp)

    # Bidirectional reference
    CreditLines.register_delete_rule(Clients, 'credit_line', NULLIFY)
    Profiles.register_delete_rule(Clients, 'profiles', NULLIFY)
    Clients.register_delete_rule(CreditLines, 'client', CASCADE)
    Clients.register_delete_rule(Profiles, 'client', CASCADE)
    Clients.register_delete_rule(Clients, 'referred_by_client', NULLIFY)

    return app
