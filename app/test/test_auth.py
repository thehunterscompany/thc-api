import json
from app.test.setup_test_auth import SetupTestDB


class TestCase(SetupTestDB):

    def tearDown(self):
        active_col = self.test_db.list_collection_names()
        for collection in active_col:
            self.test_db[collection].drop()

    def test_welcome_endpoint(self):
        res = self.app_client.get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data == 'The Hunters Company')

    def test_post_roles(self):
        role_data = {'type': 'test1', 'description': 'test case'}
        res = self.app_client.post('/roles', data=role_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['type'], 'test1')

        role_data = {'type': 'test2', 'description': 'test case'}
        res = self.app_client.post('/roles', json=role_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['type'], 'test2')

    def test_fail_duplicate_post_roles(self):
        role_data = {'type': 'test1', 'description': 'test case'}
        res = self.app_client.post('/roles', data=role_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['result']['type'], 'test1')

        res = self.app_client.post('/roles', json=role_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['result'], 'unprocessable')

    def test_post_client_type(self):
        request_data = {'employment_type': 'test1'}
        res = self.app_client.post('/client_types', data=request_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['employment_type'], 'test1')

        request_data = {'employment_type': 'test2'}
        res = self.app_client.post('/client_types', json=request_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['employment_type'], 'test2')

    def test_fail_duplicate_post_client_type(self):
        request_data = {'employment_type': 'test1'}
        res = self.app_client.post('/client_types', data=request_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['employment_type'], 'test1')

        request_data = {'employment_type': 'test1'}
        res = self.app_client.post('/client_types', json=request_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['result'], 'unprocessable')

