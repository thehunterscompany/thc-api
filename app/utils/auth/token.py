from itsdangerous import URLSafeTimedSerializer

from flask import current_app

from app.utils.constants import SECRET_KEY, SECURITY_PASSWORD_SALT


def generate_confirmation_token(email: str) -> URLSafeTimedSerializer:
    """

    :param email:
    :return:
    """
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600) -> str or bool:
    """

    :param token:
    :param expiration:
    :return
    """
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email
