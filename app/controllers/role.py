from flask import Blueprint, request
from marshmallow import ValidationError
from mongoengine import NotUniqueError

from ..collections.role import Roles
from ..schemas.role_schema import SaveRoleInput
from ..utils import response, rewrite_abort, parser_one_object, parser_all_object

bp = Blueprint('roles', __name__, url_prefix='/')


@bp.route('/roles', methods=['POST'])
def save():  # pragma: no cover
    """
    Post New Role
    """
    try:
        schema = SaveRoleInput()
        role = schema.load(request.json)
        instance = Roles(**role).save()
        return response(parser_one_object(instance)), 201

    except ValidationError as err:
        rewrite_abort(400, err)
    except NotUniqueError as err:
        rewrite_abort(422, err)
    except Exception as err:
        rewrite_abort(500, err)


@bp.route('/roles', methods=['GET'])
def get_roles():  # pragma: no cover
    try:
        roles = Roles.objects
        if len(roles):
            return response(parser_all_object(roles)), 200
        raise Exception
    except Exception as err:
        rewrite_abort(404, err)
