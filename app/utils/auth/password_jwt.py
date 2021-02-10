import base64
import datetime

import jwt


def encrypt_data(data: dict, key: str) -> str:
    """
    :param data: dict containing key value to encrypt
    :param key: key of dict to encrypt
    :return encrypted value
    """
    val_to_encrypt = data[key]
    if val_to_encrypt == "":
        raise
    encrypt_bytes = base64.b64encode(val_to_encrypt.encode("utf-8"))
    return str(encrypt_bytes, "utf-8")


def decrypt_data(encrypted_val) -> str:
    """
    :param encrypted_val
    :return: decrypted value
    """
    decoded_str = str(base64.b64decode(encrypted_val), 'utf-8')

    return decoded_str


def generate_jwt(login_user):
    if login_user:
        payload = {
            'email': login_user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, minutes=0, seconds=0),
        }

        return {
            'apiToken': jwt.encode(payload, "secret", algorithm="HS256"),
            'user': {
                'email': login_user.email,
                'role_type': login_user.role_type.type,
                'loggedIn': True}
        }
