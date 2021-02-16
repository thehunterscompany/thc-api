import json
from app.test.controllers.auth.setup_test_auth import DefaultSetup


class AuthTestCase(DefaultSetup):

    def tearDown(self):
        active_col = self.test_db.list_collection_names()
        for collection in active_col:
            if collection in ('users', 'profiles', 'credit_lines'):
                self.test_db[collection].drop()

    def test_register_login_client(self):
        payload = {'email': 'ajzpiv97@gmail.com',
                   'password': '12345',
                   'role_type': 'client',
                   'name': ['Armando',  'Jose'],
                   'last_name': ['Zubillaga', 'Prado'],
                   'age': [25, 28],
                   'personal_id': ['1111', '111223'],
                   'income': ['111111', '2323342'],
                   'employment_type': ['employee', 'self-employed'],
                   'budget': '124324',
                   'initial_payment': '41234123423',
                   'financing_value': '14324123413242314',
                   'credit_line_type': 'leasing',
                   'financing_time': '1232'}

        res = self.app_client.post('/register', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        payload = {'email': 'ajzpiv97@gmail.com',
                   'password': '12345'}

        res = self.app_client.post('/login', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['user']['loggedIn'], True)

    def test_fail_register_client(self):
        # Not unique id
        payload = {'email': 'ajzpiv97@gmail.com',
                   'password': '12345',
                   'role_type': 'client',
                   'name': "['Armando',  'Jose']",
                   'last_name': "['Zubillaga', 'Prado']",
                   'age': "[25, 28]",
                   'personal_id': "['111111', '111111']",
                   'income': "['111111', '2323342']",
                   'employment_type': "['employee', 'self-employed']",
                   }

        res = self.app_client.post('/register', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['result'], 'unprocessable')

        # Missing value
        payload = {'email': 'ajzpiv97@gmail.com',
                   'password': '12345',
                   'role_type': 'client',
                   'name': "['Armando',  'Jose']",
                   'last_name': "['Zubillaga', 'Prado']",
                   'age': "[25, 28]",
                   'personal_id': "['1113241', '1111']",
                   'income': "['111111', '2323342']",
                   'employment_type': "['employee', 'self-employed']",
                   'initial_payment': '41234123423',
                   'financing_value': '14324123413242314',
                   'credit_line_type': 'leasing',
                   'financing_time': '1232'}

        res = self.app_client.post('/register', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(data['result'], 'bad request')

        payload = {'email': 'ajzpiv97@gmail.com',
                   'password': '12345',
                   'role_type': 'client',
                   'name': "['Armando',  'Jose']",
                   'last_name': "['Zubillaga', 'Prado']",
                   'age': "[25, 28]",
                   'personal_id': "['1111', '111223']",
                   'income': "['111111', '2323342']",
                   'employment_type': "['employee', 'self-employed']",
                   'budget': '124324',
                   'initial_payment': '41234123423',
                   'financing_value': '14324123413242314',
                   'credit_line_type': 'leasing',
                   'financing_time': '1232'}

        self.app_client.post('/register', json=payload)

        payload = {'email': 'ajzpiv97@gmail.com',
                   'password': '12345',
                   'role_type': 'client',
                   'name': "['Armando',  'Jose']",
                   'last_name': "['Zubillaga', 'Prado']",
                   'age': "[25, 28]",
                   'personal_id': "['1115341', '1112523']",
                   'income': "['111111', '2323342']",
                   'employment_type': "['employee', 'self-employed']",
                   'budget': '124324',
                   'initial_payment': '41234123423',
                   'financing_value': '14324123413242314',
                   'credit_line_type': 'leasing',
                   'financing_time': '1232'}

        res = self.app_client.post('/register', json=payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['result'], 'unprocessable')

    def test_email_confirmation(self):
        res = self.app_client.get('/confirm/{}'.format("http://localhost:5000/confirm/token?token="
                                                        "ImFqenBpdjk3QGdtYWlsLmNvbSI.YCsyuw.B7pebCMPLGNF4kJtCqoyU0jMBBU"))
        self.assertEqual(res.status_code, 422)


