import pytest
from flask import Flask
from flask_socketio import SocketIO, emit
from api.server import create_app
from flask.testing import FlaskClient

@pytest.fixture
def client():
    app, socketio = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_route(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Blockchain Viewer' in response.data

def test_create_wallet(client: FlaskClient):
    response = client.post('/api/wallet/create')
    assert response.status_code == 201
    assert "address" in response.json

def test_get_blocks(client: FlaskClient):
    response = client.get('/api/blockchain/blocks')
    assert response.status_code == 200
    assert "blocks" in response.json

def test_add_transaction(client: FlaskClient):
    transaction_data = {
        "sender": "sender_address",
        "recipient": "recipient_address",
        "amount": 10
    }
    response = client.post('/api/blockchain/transaction', json=transaction_data)
    assert response.status_code == 201
    assert response.json["message"] == "Transacción añadida al bloque"

def test_mine_block(client: FlaskClient):
    response = client.get('/api/blockchain/mine')
    assert response.status_code == 200
    assert response.json["message"] == "Nuevo bloque minado"

def test_create_nft(client: FlaskClient):
    nft_data = {
        "name": "Test NFT",
        "creator": "creator_address",
        "metadata": {"image": "http://example.com/image.png", "description": "Test description"}
    }
    response = client.post('/api/nft/create', json=nft_data)
    assert response.status_code == 201
    assert response.json["message"] == "NFT creado"
    assert "nft" in response.json

def test_list_nft(client: FlaskClient):
    nft_data = {
        "name": "Test NFT",
        "creator": "creator_address",
        "metadata": {"image": "http://example.com/image.png", "description": "Test description"}
    }
    create_response = client.post('/api/nft/create', json=nft_data)
    nft_id = create_response.json["nft"]["id"]

    list_data = {
        "nft_id": nft_id,
        "price": 100
    }
    response = client.post('/api/nft/list', json=list_data)
    assert response.status_code == 200
    assert response.json["message"] == "NFT listado para la venta"

def test_buy_nft(client: FlaskClient):
    nft_data = {
        "name": "Test NFT",
        "creator": "creator_address",
        "metadata": {"image": "http://example.com/image.png", "description": "Test description"}
    }
    create_response = client.post('/api/nft/create', json=nft_data)
    nft_id = create_response.json["nft"]["id"]

    buy_data = {
        "nft_id": nft_id,
        "buyer": "buyer_address"
    }
    response = client.post('/api/nft/buy', json=buy_data)
    assert response.status_code == 200
    assert response.json["message"] == "NFT comprado"
    assert response.json["nft"]["owner"] == "buyer_address"
