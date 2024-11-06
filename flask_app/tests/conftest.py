import pytest
from flask_jwt_extended import create_access_token
from src.app import create_app


@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def jwt_token(app):
    with app.app_context():
        token = create_access_token(identity="test_user")
        yield token
