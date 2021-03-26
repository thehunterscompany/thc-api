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
from app.schemas.user_schema import SaveUserInput
from app.utils import response, rewrite_abort, parser_one_object
from app.utils.auth.password_jwt import *
from app.utils.auth.token import generate_confirmation_token, confirm_token
from app.utils.config.email import send_mail

bp = Blueprint('auth', __name__, url_prefix='/')
logger = logging.getLogger(__name__)


class AuthError(Exception):  # pragma: no cover
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@bp.route('/register', methods=['POST'])
def register():  # pragma: no cover
    """
    Register User
    """
    new_user_instance = None

    try:
        # User
        new_user_data = {'email': request.json['email'],
                         'password': request.json['password'],
                         'role_type': request.json['roleType'],
                         'verified': request.json['verified'] if request.json.get('verified') else False
                         }

        new_user = SaveUserInput().load(new_user_data)
        new_user['password'] = encrypt_data(new_user, 'password')
        new_user['role_type'] = Roles.objects.get(type=new_user['role_type'])
        new_user_instance = Users(**new_user).save()

        if 'Cliente' in new_user_instance.role_type.type:
            client_data = {'user': new_user_instance, 'referred_by_non_related': request.json['referred_by_non_related']
                           if request.json.get('referred_by_non_related') else 'N/A',
                           'referred_by_client': request.json['referred_by_client']
                           if request.json.get('referred_by_client') else 'N/A'}

            new_client = SaveClientInput().load(client_data)
            Clients(**new_client).save()

    except (ValidationError, KeyError) as err:
        try:
            new_user_instance.delete()
        except AttributeError:
            pass
        finally:
            rewrite_abort(400, err)

    except NotUniqueError as err:
        try:
            new_user_instance.delete()
        except AttributeError:
            pass
        finally:
            rewrite_abort(422, err)

    except Exception as err:
        try:
            new_user_instance.delete()
        except AttributeError:
            pass
        finally:
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
def confirm_email(token):  # pragma: no cover
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
def login():  # pragma: no cover
    """
    User login
    """
    try:
        user = Users.objects(email=request.json['email']).first()
        if user is None:
            raise AuthError({'code': 'Not Found',
                             'description': 'Este usuario no fue encontrado'
                                            ' en nuestros sistemas!'
                             }, 404)

        else:
            if user.verified:
                if request.json['password'] == decrypt_data(user.password):
                    return response(generate_jwt(user))
                else:
                    raise AuthError({'code': 'Unauthorized',
                                     'description': 'Tu contraseña es incorrecta.'
                                     }, 401)
            else:
                err = 'Usted no ha confirmado su cuenta. Por favor revise su correo electronico ' \
                      'y haga click en el link que le enviamos.'
                rewrite_abort(403, err)

    except AuthError as err:
        rewrite_abort(err.status_code, err.error['description'])
