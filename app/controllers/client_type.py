from flask import Blueprint, request, abort, jsonify
from marshmallow import ValidationError
from mongoengine import NotUniqueError
from bson.objectid import ObjectId
from ..collections.client_type import ClientTypes
from ..schemas.client_type_schema import *
from ..utils import *

bp = Blueprint('client_types', __name__, url_prefix='/')


@bp.route('/client-types', methods=['GET'])
def table():
    try:
        search, page, per_page = unpack_url_params()

        pipeline = [
            {
                '$lookup': {
                    'from': 'documents',
                    'localField': 'documents',
                    'foreignField': '_id',
                    'as': 'documents'
                }
            },
            {'$unwind': '$documents'},
            {
                '$group': {
                    '_id': '$_id',
                    'id': {'$first': {'$toString': '$_id'}},
                    'employment_type': {'$first': '$employment_type'},
                    'documents': {
                        '$push': {
                            'id': {'$toString': '$documents._id'},
                            'active': '$documents.active',
                            'name': '$documents.name',
                        }
                    },
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
            },
            {
                '$match': {
                    '$or': [
                        {'employment_type': {'$regex': search, '$options': 'i'}},
                        {'documents.name': {'$regex': search, '$options': 'i'}},
                    ]
                }
            }
        ]

        pipeline = pipeline + pagination(page, per_page, {'name': 1})
        documents = ClientTypes.objects().aggregate(pipeline)

        return response(default_paginate_schema(documents, page, per_page))

    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/client-types/<id>', methods=['GET'])
def get(id):
    try:
        client_type = ClientTypes.objects.get(id=id)
        client_type = parser_one_object(client_type)

        return response(client_type)

    except ClientTypes.DoesNotExist as not_found:
        rewrite_abort(404, not_found)
    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/client-types', methods=['POST'])
def save():
    """
    Post New Client Type
    """
    try:
        schema = SaveClientTypeInput()
        client_type = schema.load(request.json)
        instance = ClientTypes(**client_type).save()
        return response(parser_one_object(instance)), 201

    except ValidationError as err:
        rewrite_abort(400, err)
    except NotUniqueError as err:
        rewrite_abort(422, err)
    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/client-types/<id>', methods=['PUT'])
def update(id):
    try:
        schema = UpdateClientTypeInput()
        client_type = schema.load(request.json)

        document_ids = [ObjectId(document) for document in client_type['documents']]
        client_type['documents'] = document_ids

        instance = update_or_create(ClientTypes, {'id': id}, client_type)

        return response(parser_one_object(instance))

    except (ValidationError or NotUniqueError) as err:
        rewrite_abort(400, err)
    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/client-types/<id>', methods=['DELETE'])
def delete(id):
    try:
        client_type = ClientTypes.objects.get(id=id)
        client_type.delete()

        return response(), 204

    except ClientTypes.DoesNotExist as not_found:
        rewrite_abort(404, not_found)
    except Exception as err:
        rewrite_abort(500, err)
