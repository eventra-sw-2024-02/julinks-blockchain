from flask import Blueprint, request, jsonify
from blockchain.wallet.wallet import Wallet

wallet_routes = Blueprint('wallet_routes', __name__)

wallets = {}  # Almacenamiento temporal de billeteras

@wallet_routes.route('/create', methods=['POST'])
def create_wallet():
    wallet = Wallet()
    wallets[wallet.address] = wallet
    return jsonify({"message": "Billetera creada", "address": wallet.address}), 201

@wallet_routes.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    wallet = wallets.get(address)
    if not wallet:
        return jsonify({"error": "Billetera no encontrada"}), 404
    return jsonify({"address": address, "balance": wallet.get_balance()}), 200