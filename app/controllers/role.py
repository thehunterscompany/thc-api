from flask import Blueprint, request, abort, jsonify
from mongoengine import NotUniqueError

from ..collections.role import Roles
from ..utils import response

bp = Blueprint('roles', __name__, url_prefix='/')


@bp.route('/roles', methods=['POST'])
def post_roles():
    """
    Post New Role
    """
    if request.content_type == 'application/json':
        data = request.get_json()
    else:
        data = request.form
    try:
        role = Roles(type=data['type'], description=data['description'])
        role.save()
        return jsonify({'result': role.format()})

    except NotUniqueError:
        abort(422)

    except Exception:
        abort(400)
