from flask import Blueprint, request, abort, jsonify
from ..utils import response

bp = Blueprint('document', __name__, url_prefix='/')


@bp.route('/documents', methods=['GET'])
def table():
    return jsonify(response('get all or specific document with pagination'))


@bp.route('/documents/<id>', methods=['GET'])
def get():
    return jsonify(response('get specific document'))


@bp.route('/documents', methods=['POST'])
def save():
    return jsonify(response('create document'))


@bp.route('/documents/<id>', methods=['UPDATE'])
def update():
    return jsonify(response('update document'))


@bp.route('/documents/<id>', methods=['DELETE'])
def delete():
    return jsonify(response('delete document'))

