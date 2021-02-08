import os

DATABASE_NAME = os.getenv('DATABASE_NAME', 'thc')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME', 'thc_test')
DATABASE_PORT = int(os.getenv('DATABASE_PORT', 27017))

