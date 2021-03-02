import unittest

from app.test.integration.controllers.setup_test_db import SetupTestDB


class UtilsSetup(unittest.TestCase, SetupTestDB):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_db, cls.app_client = cls.start_db()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.close_db()
