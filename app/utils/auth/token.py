import os

from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email: str) -> URLSafeTimedSerializer:
    """

    :param email:
    :return:
    """
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('SECURITY_PASSWORD_SALT'))


def confirm_token(token, expiration=4000) -> str:
    """

    :param token:
    :param expiration:
    :return
    """
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        email = serializer.loads(
            token,
            salt=os.getenv('SECURITY_PASSWORD_SALT'),
            max_age=expiration
        )
    except Exception as err:
        return '{}'.format(err)
    return email
