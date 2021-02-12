from flask import jsonify
from .common import response


def error_handler(app):
    @app.errorhandler(400)
    def bad_request(e):
        return __get_message(e, 'Bad request', 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return __get_message(e, 'Unauthorized', 401)

    @app.errorhandler(404)
    def page_not_found(e):
        return __get_message(e, 'Not found', 404)

    @app.errorhandler(405)
    def not_allowed(e):
        return __get_message(e, 'Method not allowed', 405)

    @app.errorhandler(422)
    def unprocessable(e):
        return __get_message(e, 'Unprocessable', 422)

    @app.errorhandler(500)
    def server_error(e):
        return __get_message(e, 'Server error', 500)

    def __get_message(error, default_message, code):
        message = default_message
        if 'message' in error.description:
            message = error.description['message']

        return jsonify(response(message)), code
