import pytest
from api.server import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

def test_create_wallet(client):
    response = client.post('/api/wallet/create')
    assert response.status_code == 201
    assert "address" in response.json
