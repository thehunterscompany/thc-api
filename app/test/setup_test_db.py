import pymongo

from app import create_app
from app.utils.contants import *


class SetupTestDB:
    @staticmethod
    def start_db():
        my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        db_list = my_client.list_database_names()
        if TEST_DATABASE_NAME in db_list:
            my_client.drop_database(TEST_DATABASE_NAME)
        test_db = my_client[TEST_DATABASE_NAME]
        app = create_app(testing=True)

        app_client = app.test_client()

        return test_db, app_client

    @staticmethod
    def close_db():
        my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        my_client.drop_database(TEST_DATABASE_NAME)
