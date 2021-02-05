import json

from app import create_app
from app.collections.role import Roles
from app.test.test_setup import SetupTestDB
from app.utils.contants import *


class TestCase(SetupTestDB):

    def test_welcome_endpoint(self):
        res = self.app_client.get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data == 'The Hunters Company')

    def test_post_roles(self):
        role_data = {'type': 'test1', 'description': 'test case'}
        res = self.app_client.post('/roles', json=role_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

