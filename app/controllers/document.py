from flask import Blueprint, request, abort, jsonify
from mongoengine.queryset import NotUniqueError
from ..utils import response, parser_one_object, rewrite_abort
from ..collections import Documents

bp = Blueprint('document', __name__, url_prefix='/')


@bp.route('/documents', methods=['GET'])
def table():
    return jsonify(response('get all or specific document with pagination'))


@bp.route('/documents/<id>', methods=['GET'])
def get():
    return jsonify(response('get specific document'))


@bp.route('/documents', methods=['POST'])
def save():
    try:
        document = request.get_json()
        instance = Documents(**document).save()

        return jsonify(response(parser_one_object(instance)))

    except Exception as err:
        rewrite_abort(500, err)
    except NotUniqueError:
        abort(400)


@bp.route('/documents/<id>', methods=['UPDATE'])
def update():
    return jsonify(response('update document'))


@bp.route('/documents/<id>', methods=['DELETE'])
def delete():
    return jsonify(response('delete document'))
