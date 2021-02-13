from flask import Blueprint, request, abort, jsonify
from mongoengine import NotUniqueError

from ..collections.client_type import ClientTypes
from ..utils import response, rewrite_abort, parser_one_object

bp = Blueprint('client_types', __name__, url_prefix='/')


@bp.route('/client_types', methods=['POST'])
def post_client_type():
    """
    Post New Client Type
    """
    if request.content_type == 'application/json':
        data = request.get_json()
    else:
        data = request.form
    try:
        client_type = ClientTypes(employment_type=data['employment_type'],
                                  documents=None)
        instance = client_type.save()
        return response(parser_one_object(instance)), 201

    except NotUniqueError as err:
        rewrite_abort(422, err)

    except Exception as err:
        rewrite_abort(404, err)
