import logging
from flask import Blueprint, request, redirect, url_for, render_template
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
from app.utils.auth.token import generate_confirmation_token, confirm_token
from app.utils.config.email import send_mail

bp = Blueprint('auth', __name__, url_prefix='/')
logger = logging.getLogger(__name__)


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@bp.route('/register', methods=['POST'])
def register():
    """
    Register User
    """
    profiles = []
    credit_line_instance = None
    new_user_instance = None

    try:
        request.json['password'] = encrypt_data(request.json, 'password')
        request.json['role_type'] = Roles.objects.get(type=request.json['role_type'])
        client_instance = SaveClientInput().load(request.json, unknown='EXCLUDE')
        new_user_instance = Clients(**client_instance).save()

    except NotUniqueError as err:
        rewrite_abort(422, err)
    except Exception as err:
        rewrite_abort(400, err)

    try:
        for profile in request.json['profiles']:
            profile['client_type'] = ClientTypes.objects.get(employment_type=profile['client_type'])
            profile['client'] = new_user_instance
            profiles.append(profile)
        profiles = SaveProfileInput(many=True).load(profiles, unknown='EXCLUDE')
        for i in range(len(profiles)):
            profiles[i] = Profiles(**profiles[i]).save()

    except ValidationError as err:
        new_user_instance.delete()

        rewrite_abort(400, err)
    except NotUniqueError as err:
        new_user_instance.delete()

        rewrite_abort(422, err)
    except Exception as err:
        new_user_instance.delete()
        rewrite_abort(500, err)

    # Credit Line
    try:
        schema = SaveCreditLineInput()
        request.json['credit_line']['client'] = new_user_instance
        credit_line = schema.load(request.json['credit_line'], unknown='EXCLUDE')
        credit_line_instance = CreditLines(**credit_line).save()

    except ValidationError as err:
        new_user_instance.delete()

        rewrite_abort(400, err)
    except Exception as err:
        new_user_instance.delete()
        rewrite_abort(500, err)

    try:
        token = generate_confirmation_token(new_user_instance.email)

        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('send_confirmation.html', confirm_url=confirm_url)
        subject = "Please confirm your email"

        send_mail(new_user_instance.email, html, subject)

        return response(parser_one_object(new_user_instance)), 201

    except Exception as err:
        new_user_instance.delete()
        rewrite_abort(422, err)


@bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = confirm_token(token)
        if 'Signature' and 'age' in email.split():
            raise AuthError({
                'code': 'Bad Request',
                'description': 'The Url has expired!'
            }, 400)
        if 'Signature' and 'match' in email.split():
            raise AuthError({
                'code': 'Unauthorized',
                'description': 'Signature does not match!'
            }, 401)

        user = Users.objects(email=email).first()

        if user is None:
            raise AuthError({
                'code': 'Not Found',
                'description': 'User Not Found!'
            }, 404)

        if user.verified:
            raise AuthError({
                'code': 'Conflict',
                'description': 'User already verified! Please login!'
            }, 409)

    except AuthError as err:
        return render_template('confirmation_error.html', status_code=err.status_code,
                               error_type=err.error['code'], description=err.error['description'])

    user.verified = True
    user.save()
    return render_template('confirmation_valid.html')


@bp.route('/login', methods=['POST'])
def login():
    """
    User login
    """
    try:
        user = Users.objects(email=request.json['email']).first()
        if user is None:
            raise AuthError({'code': 'Not Found',
                                     'description': 'User was not'
                                                    ' found in our database'
                             }, 404)
    except AuthError as err:
        rewrite_abort(err.status_code, err.error['description'])

    else:
        if user.verified:
            try:
                if request.json['password'] == decrypt_data(user.password):
                    return response(generate_jwt(user))
                else:
                    raise AuthError({'code': 'Unauthorized',
                                     'description': 'Your password is incorrect!'
                                     }, 401)
            except AuthError as err:
                rewrite_abort(err.status_code, err.error['description'])
        else:
            err = 'User has not confirm registration! Please check email.'
            rewrite_abort(403, err)
