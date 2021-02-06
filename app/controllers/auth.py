from flask import Blueprint, request, abort, jsonify
from mongoengine import NotUniqueError

from app.collections.client_type import ClientType
from app.collections.credit_line import CreditLines
from app.collections.profile import Profiles
from app.collections.role import Roles
from app.collections.client import Clients

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    role_type = request.form['role_type']
    role = Roles.objects.get(type=role_type)
    names = request.form['name']
    last_names = request.form['last_name']
    ages = request.form['age']
    personal_ids = request.form['personal_id']
    incomes = request.form['income']
    employment_types = request.form['employment_type']

    profiles = []
    # Profiles
    for i in range(len(names)):
        profiles.append(Profiles(name=names[i], last_name=last_names[i], age=ages[i], personal_id=personal_ids[i],
                        income=incomes[i],
                        client_type=ClientType(employment_type=employment_types[i], document=None)))
    for profile in profiles:
        try:
            profile.save()
        except NotUniqueError:
            abort(422)

    # Credit Line
    budget = request.form['budget']
    initial_payment = request.form['initial_payment']
    financing_value = request.form['financing_value']
    credit_line_type = request.form['credit_line_type']
    financing_time = request.form['financing_time']

    credit_line = CreditLines(budget=budget, initial_payment=initial_payment, financing_value=financing_value,
                              credit_line_type=credit_line_type, financing_time=financing_time)
    credit_line.save()

    try:
        client = Clients(email=email, password=password, role=role, profile=profiles, credit_line=credit_line,
                         number_owners=len(profiles), referred_by='me')
        client.save()

        return jsonify({'success': True, 'result': client.format()})

    except NotUniqueError:
        abort(422)


@bp.route('/login', methods=['POST'])
def login():
    return 'login'


@bp.route('/roles', methods=['POST'])
def post_roles():
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
        abort(404)


@bp.route('/client_types', methods=['POST'])
def post_client_type():
    if request.content_type == 'application/json':
        data = request.get_json()
    else:
        data = request.form
    try:
        client_type = ClientType(employment_type=data['employment_type'], documents=None)
        client_type.save()
        return jsonify({'result': client_type.format()})

    except NotUniqueError:
        abort(422)

    except Exception:
        abort(404)
