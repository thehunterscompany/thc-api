from flask import Blueprint, request, abort, jsonify
from marshmallow import ValidationError
from mongoengine.queryset import NotUniqueError
from ..utils import response, parser_one_object, rewrite_abort
from ..collections import Documents
from ..schemas.document_schema import SaveDocumentInput

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
        schema = SaveDocumentInput()
        document = schema.load(request.json)
        instance = Documents(**document).save()

        return jsonify(response(parser_one_object(instance)))

    except ValidationError as validation_err:
        rewrite_abort(400, validation_err)
    except NotUniqueError:
        abort(400)
    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/documents/<id>', methods=['UPDATE'])
def update():
    return jsonify(response('update document'))


@bp.route('/documents/<id>', methods=['DELETE'])
def delete():
    return jsonify(response('delete document'))
