import ast
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from mongoengine import NotUniqueError

from app.collections.client_type import ClientTypes
from app.collections.credit_line import CreditLines
from app.collections.profile import Profiles
from app.collections.role import Roles
from app.collections.client import Clients
from app.collections.user import Users
from app.schemas.client_schema import SaveClientInput
from app.schemas.credit_line_schema import SaveCreditLineInput
from app.schemas.profile_schema import SaveProfileInput
from app.utils import response, rewrite_abort, parser_one_object
from app.utils.auth.password_jwt import *
from app.utils.config.email import send_mail

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/register', methods=['POST'])
def register():
    """
    Register User
    """
    profiles = []
    credit_line_instance = None
    new_user_instance = None
    try:
        for profile in request.json['profiles']:
            profile['client_type'] = ClientTypes.objects.get(employment_type=profile['client_type'])
            profiles.append(profile)
        profiles = SaveProfileInput(many=True).load(profiles, unknown='EXCLUDE')
        for i in range(len(profiles)):
            profiles[i] = Profiles(**profiles[i]).save()

    except ValidationError as err:
        rewrite_abort(400, err)
    except NotUniqueError as err:
        rewrite_abort(422, err)
    except Exception as err:
        rewrite_abort(500, err)

    # Credit Line
    try:
        schema = SaveCreditLineInput()
        credit_line = schema.load(request.json['credit_line'], unknown='EXCLUDE')
        credit_line_instance = CreditLines(**credit_line).save()

    except ValidationError as err:
        for profile in profiles:
            profile.delete()
        rewrite_abort(400, err)
    except Exception as err:
        for profile in profiles:
            profile.delete()
        rewrite_abort(500, err)

    try:
        request.json['password'] = encrypt_data(request.json, 'password')
        request.json['role_type'] = Roles.objects.get(type=request.json['role_type'])
        request.json['profiles'] = profiles
        request.json['credit_line'] = credit_line_instance

        client_instance = SaveClientInput().load(request.json, unknown='EXCLUDE')

        new_user_instance = Clients(**client_instance).save()

        send_mail()

        return response(parser_one_object(new_user_instance)), 201

    except NotUniqueError as err:
        new_user_instance.delete()
        rewrite_abort(422, err)

    except Exception as err:
        new_user_instance.delete()
        rewrite_abort(400, err)


@bp.route('/login', methods=['POST'])
def login():
    """
    User login
    """

    try:
        data = request.json

        user = Users.objects.get(
            email=data['email']
        )

        if not user.verified:
            if data['password'] == decrypt_data(user.password):
                return response(generate_jwt(user))
            else:
                err = 'Your password is incorrect.'
                rewrite_abort(401, err)

    except Exception as err:
        rewrite_abort(422, err)
