import json
import os

from app.test.integration.controllers.auth.test_setup_auth import DefaultSetup
from app.utils.auth.token import generate_confirmation_token


class AuthTestCase(DefaultSetup):
    os.environ['SECRET_KEY'] = 'secret_key'
    os.environ['SECURITY_PASSWORD_SALT'] = 'salt'

    def tearDown(self):
        self.app_client.application.config["MAIL_DEFAULT_SENDER"] = None
        active_col = self.test_db.list_collection_names()
        for collection in active_col:
            if collection in ('users', 'profiles', 'credit_lines'):
                self.test_db[collection].drop()

    def test_register_login_client(self):
        self.app_client.application.config["MAIL_DEFAULT_SENDER"] = 'ajzpiv97@gmail.com'
        payload = {"email": "ajzpiv97@gmail.com",
                   "password": "12345",
                   "role_type": "client",
                   "referred_by_non_related": "me",
                   "verified": True
                   }

        res = self.app_client.post('/register', json=payload)
        self.assertEqual(res.status_code, 201)

        payload = {'email': 'ajzpiv97@gmail.com',
                   'password': '12345'}

        res = self.app_client.post('/login', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['user']['loggedIn'], True)

    def test_confirm_email(self):
        payload = {"email": "ajzpiv97@gmail.com",
                   "password": "12345",
                   "role_type": "client",
                   "referred_by_non_related": "me",
                   }
        self.app_client.post('/register', json=payload)
        token = generate_confirmation_token(payload['email'])
        res = self.app_client.get('/confirm/{}'.format(token))
        self.assertEqual(res.status_code, 200)

    def test_fail_register_client_failed_email(self):
        # Fail to send email
        payload = {"email": "ajzpiv97@gmail.com",
                   "password": "12345",
                   "role_type": "client",
                   }

        res = self.app_client.post('/register', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['result'], 'unprocessable')

        # Missing value
        payload = {"email": "ajzpiv98@gmail.com",
                   "password": "12345",
                   }

        res = self.app_client.post('/register', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['result'], 'bad request')

    def test_fail_login(self):
        self.app_client.application.config["MAIL_DEFAULT_SENDER"] = 'ajzpiv97@gmail.com'

        # Wrong password
        payload = {"email": "ajzpiv97@gmail.com",
                   "password": "12345",
                   "role_type": "client",
                   "verified": True
                   }
        self.app_client.post('/register', json=payload)

        payload = {'email': 'ajzpiv97@gmail.com',
                   'password': '123456'}

        res = self.app_client.post('/login', json=payload)
        self.assertEqual(res.status_code, 401)

        # User not found
        payload = {'email': 'ajz@gmail.com',
                   'password': '123456'}

        res = self.app_client.post('/login', json=payload)
        self.assertEqual(res.status_code, 404)

    def test_fail_login_user_not_verified(self):
        self.app_client.application.config["MAIL_DEFAULT_SENDER"] = 'ajzpiv97@gmail.com'

        # Wrong password
        payload = {"email": "ajzpiv97@gmail.com",
                   "password": "12345",
                   "role_type": "client",
                   }
        self.app_client.post('/register', json=payload)

        payload = {'email': 'ajzpiv97@gmail.com',
                   'password': '123456'}

        res = self.app_client.post('/login', json=payload)
        self.assertEqual(res.status_code, 403)



