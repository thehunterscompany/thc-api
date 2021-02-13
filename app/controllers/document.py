from flask import Blueprint, request, abort, jsonify
from marshmallow import ValidationError
from mongoengine.queryset import NotUniqueError
from ..collections import Documents
from ..schemas.document_schema import *
from ..utils import *

bp = Blueprint('document', __name__, url_prefix='/')


@bp.route('/documents', methods=['GET'])
def table():
    try:
        search, page, per_page = unpack_url_params()

        pipeline = [
            {
                '$match': {
                    '$or': [
                        {'name': {'$regex': search, '$options': 'i'}},
                        {'active': {'$regex': search, '$options': 'i'}}
                    ]
                }
            },
            {
                '$set': {
                    'id': {'$toString': '$_id'}
                }
            },
            {
                '$project': {
                    '_id': 0
                }
            }
        ]

        pipeline = pipeline + pagination(page, per_page, {'name': 1})
        documents = Documents.objects().aggregate(pipeline)

        return response(default_paginate_schema(documents, page, per_page))

    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/documents/<id>', methods=['GET'])
def get(id):
    try:
        document = Documents.objects.get(id=id)
        document = parser_one_object(document)

        return response(document)

    except Documents.DoesNotExist as not_found:
        rewrite_abort(404, not_found)
    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/documents', methods=['POST'])
def save():
    try:
        schema = SaveDocumentInput()
        document = schema.load(request.json)
        instance = Documents(**document).save()

        return response(parser_one_object(instance)), 201

    except (ValidationError or NotUniqueError) as err:
        rewrite_abort(400, err)
    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/documents/<id>', methods=['PUT'])
def update(id):
    try:
        schema = UpdateDocumentInput()
        document = schema.load(request.json)
        instance = update_or_create(Documents, {'id': id}, document)

        return response(parser_one_object(instance))

    except (ValidationError or NotUniqueError) as err:
        rewrite_abort(400, err)
    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/documents/<id>', methods=['DELETE'])
def delete(id):
    try:
        document = Documents.objects.get(id=id)
        document.delete()

        return response(), 204

    except Documents.DoesNotExist as not_found:
        rewrite_abort(404, not_found)
    except Exception as err:
        rewrite_abort(500, err)
