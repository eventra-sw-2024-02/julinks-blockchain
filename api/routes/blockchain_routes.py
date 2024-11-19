from flask import Blueprint, request, jsonify
from blockchain.core.blockchain import Blockchain

def create_blockchain_routes(blockchain):
    blockchain_routes = Blueprint('blockchain_routes', __name__)

    @blockchain_routes.route('/blocks', methods=['GET'])
    def get_blocks():
        return jsonify({"blocks": [block.__dict__ for block in blockchain.chain]}), 200

    @blockchain_routes.route('/transaction', methods=['POST'])
    def add_transaction():
        data = request.json
        try:
            blockchain.add_transaction(data['sender'], data['recipient'], data['amount'])
            return jsonify({"message": "Transacción añadida al bloque"}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @blockchain_routes.route('/mine', methods=['GET'])
    def mine_block():
        blockchain.mine_pending_transactions()
        return jsonify({"message": "Nuevo bloque minado"}), 200

    return blockchain_routes