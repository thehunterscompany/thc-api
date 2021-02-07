import json
from app.test.setup_test_db import SetupTestDB


class TestCase(SetupTestDB):

    def tearDown(self):
        active_col = self.test_db.list_collection_names()
        if len(active_col) > 0:
            for collection in active_col:
                self.test_db[collection].drop()

    def test_welcome_endpoint(self):
        res = self.app_client.get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data == 'The Hunters Company')

    def test_post_roles(self):
        payload = {'type': 'test1', 'description': 'test case'}
        res = self.app_client.post('/roles', data=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['type'], 'test1')

        payload = {'type': 'test2', 'description': 'test case'}
        res = self.app_client.post('/roles', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['type'], 'test2')

    def test_fail_duplicate_post_roles(self):
        payload = {'type': 'test1', 'description': 'test case'}
        res = self.app_client.post('/roles', data=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['result']['type'], 'test1')

        res = self.app_client.post('/roles', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['result'], 'unprocessable')

    def test_post_client_type(self):
        payload = {'employment_type': 'test1'}
        res = self.app_client.post('/client_types', data=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['employment_type'], 'test1')

        payload = {'employment_type': 'test2'}
        res = self.app_client.post('/client_types', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['employment_type'], 'test2')

    def test_fail_duplicate_post_client_type(self):
        payload = {'employment_type': 'test1'}
        res = self.app_client.post('/client_types', data=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['result']['employment_type'], 'test1')

        payload = {'employment_type': 'test1'}
        res = self.app_client.post('/client_types', json=payload)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['result'], 'unprocessable')
