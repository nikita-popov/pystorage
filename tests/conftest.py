import base64
import os
import pytest
import tempfile

# from werkzeug.security import generate_password_hash

from pystorage import create_app
from config import Config as config


@pytest.fixture(scope='module')
def app():
    """Фикстура для создания экземпляра приложения."""
    upload_dir = tempfile.TemporaryDirectory()
    os.environ['SECRET_KEY'] = 'test-secret-key'
    app = create_app(config)
    app.config.update({
        'TESTING': True,
        'UPLOAD_FOLDER': upload_dir.name,
        'USERS': {
            'testuser': 'testpass'
        },
        'WTF_CSRF_ENABLED': False
    })

    with app.app_context():
        yield app
        upload_dir.cleanup()


@pytest.fixture(scope='module')
def client(app):
    """Фикстура для тестового клиента основного приложения."""
    return app.test_client()


@pytest.fixture
def auth_client(client):
    """Аутентифицируемся как тестовый пользователь"""
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    return client


@pytest.fixture
def api_headers():
    """Заголовки для Basic Auth"""
    creds = base64.b64encode(b'testuser:testpass').decode('utf-8')
    return {'Authorization': f'Basic {creds}'}
