from flask import Blueprint, request, jsonify
from blockchain.nfts.nft import NFT
from blockchain.nfts.marketplace import Marketplace

nft_routes = Blueprint('nft_routes', __name__)

marketplace = Marketplace()
nfts = {}  # Almacenamiento temporal de NFTs

@nft_routes.route('/nft/create', methods=['POST'])
def create_nft():
    data = request.json
    nft = NFT(name=data['name'], creator=data['creator'], metadata=data['metadata'])
    nfts[nft.id] = nft
    return jsonify({"message": "NFT creado", "nft": nft.__dict__}), 201

@nft_routes.route('/nft/list', methods=['POST'])
def list_nft():
    data = request.json
    nft_id = data['nft_id']
    price = data['price']
    if nft_id not in nfts:
        return jsonify({"error": "NFT no encontrado"}), 404
    marketplace.list_nft(nfts[nft_id], price)
    return jsonify({"message": "NFT listado para la venta"}), 200

@nft_routes.route('/nft/buy', methods=['POST'])
def buy_nft():
    data = request.json
    nft_id = data['nft_id']
    buyer = data['buyer']
    try:
        nft = marketplace.buy_nft(nft_id, buyer)
        return jsonify({"message": "NFT comprado", "nft": nft.__dict__}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
