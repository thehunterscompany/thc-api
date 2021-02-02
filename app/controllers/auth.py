from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/register', methods=['POST'])
def register():
    return 'register'

@bp.route('/login', methods=['POST'])
def login():
    return 'login'
