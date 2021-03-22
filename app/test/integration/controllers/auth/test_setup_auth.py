import unittest

from app.test.integration.controllers.setup_test_db import SetupTestDB


class DefaultSetup(SetupTestDB, unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Setup Data
        cls.test_db, cls.app_client = cls.start_db()
        roles_col = cls.test_db["roles"]
        roles_data = [{"type": "admin", "description": ""},
                      {"type": "client", "description": ""},
                      {"type": "real-estate", "description": ""}]

        for data in roles_data:
            roles_col.insert_one(data)

        client_type = cls.test_db["client_types"]
        client_type_data = [{"employment_type": "employee"},
                            {"employment_type": "self-employed"},
                            {"employment_type": "military"}]

        for data in client_type_data:
            client_type.insert_one(data)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.close_db()
