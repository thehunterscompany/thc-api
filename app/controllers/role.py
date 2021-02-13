from flask import Blueprint, request, abort, jsonify
from mongoengine import NotUniqueError

from ..collections.role import Roles
from ..schemas.role_schema import SaveRoleInput
from ..utils import response, rewrite_abort, parser_one_object

bp = Blueprint('roles', __name__, url_prefix='/')


@bp.route('/roles', methods=['POST'])
def post_roles():
    """
    Post New Role
    """
    try:
        schema = SaveRoleInput()
        role = schema.load(request.json)
        instance = Roles(**role).save()
        return response(parser_one_object(instance)), 201

    except NotUniqueError as err:
        rewrite_abort(422, err)

    except Exception as err:
        rewrite_abort(404, err)
