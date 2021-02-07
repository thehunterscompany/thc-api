import unittest

import pymongo

from app import create_app
from app.utils.contants import *


class SetupTestDB(unittest.TestCase):

    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    app = create_app(testing=True)
    app_client = app.test_client()

    @classmethod
    def setUpClass(cls) -> None:
        cls.db_list = cls.my_client.list_database_names()
        if TEST_DATABASE_NAME in cls.db_list:
            cls.my_client.drop_database(TEST_DATABASE_NAME)
        cls.test_db = cls.my_client[TEST_DATABASE_NAME]
        cls.app = create_app(testing=True)

        cls.app_client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.my_client.drop_database(TEST_DATABASE_NAME)
