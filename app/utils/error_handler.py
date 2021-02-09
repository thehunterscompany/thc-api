from flask import jsonify
from .common import response

def error_handler(app):
    @app.errorhandler(400)
    def page_not_found(e):
        return jsonify(response('bad request')), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(response('not found')), 404

    @app.errorhandler(405)
    def unprocessable(e):
        return jsonify(response('method not allowed')), 405

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify(response('unprocessable')), 422
