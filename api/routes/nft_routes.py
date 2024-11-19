from flask import Blueprint, request, jsonify
from blockchain.nfts.nft import NFT
from blockchain.core.blockchain import Blockchain

def create_nft_routes(blockchain):
    nft_routes = Blueprint('nft_routes', __name__)

    @nft_routes.route('/create', methods=['POST'])
    def create_nft():
        data = request.json
        nft = blockchain.create_nft(name=data['name'], creator=data['creator'], metadata=data['metadata'])
        return jsonify({"message": "NFT creado", "nft": nft.__dict__}), 201

    @nft_routes.route('/list', methods=['POST'])
    def list_nft():
        data = request.json
        nft_id = data['nft_id']
        price = data['price']
        try:
            nft = blockchain.list_nft(nft_id, price)
            return jsonify({"message": "NFT listado para la venta", "nft": nft.__dict__}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @nft_routes.route('/buy', methods=['POST'])
    def buy_nft():
        data = request.json
        nft_id = data['nft_id']
        buyer = data['buyer']
        try:
            nft = blockchain.buy_nft(nft_id, buyer)
            return jsonify({"message": "NFT comprado", "nft": nft.__dict__}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    return nft_routes