import pytest

from src.app import create_app
from src.extensions import db

@pytest.fixture
def app():
    yield create_app()

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def db(app):
    with app.app_context():
        yield app.extensions['sqlalchemy'].db