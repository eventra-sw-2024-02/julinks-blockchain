from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from api.routes.wallet_routes import wallet_routes
from api.routes.blockchain_routes import create_blockchain_routes
from api.routes.nft_routes import create_nft_routes
from api.routes.smart_contract_routes import smart_contract_routes
from blockchain.core.blockchain import Blockchain
from datetime import datetime

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)

    # Initialize the blockchain
    julinks = Blockchain()

    # Register the Blueprints
    app.register_blueprint(wallet_routes, url_prefix='/api/wallet')
    app.register_blueprint(create_blockchain_routes(julinks), url_prefix='/api/blockchain')
    app.register_blueprint(create_nft_routes(julinks), url_prefix='/api/nft')
    app.register_blueprint(smart_contract_routes, url_prefix='/api/contract')

    @app.route('/')
    def index():
        return render_template('index.html')

    @socketio.on('connect')
    def handle_connect(auth=None):
        emit('blockchain_update', {'blocks': [block_to_dict(block) for block in julinks.chain]})

    @socketio.on('request_blockchain')
    def handle_request_blockchain():
        emit('blockchain_update', {'blocks': [block_to_dict(block) for block in julinks.chain]})

    @socketio.on('mine_block')
    def handle_mine_block():
        julinks.mine_pending_transactions()
        emit('blockchain_update', {'blocks': [block_to_dict(block) for block in julinks.chain]}, broadcast=True)

    def block_to_dict(block):
        block_dict = block.__dict__.copy()
        for key, value in block_dict.items():
            if isinstance(value, datetime):
                block_dict[key] = value.isoformat()
            elif isinstance(value, list):
                block_dict[key] = [transaction_to_dict(tx) for tx in value]
        return block_dict

    def transaction_to_dict(transaction):
        tx_dict = transaction.copy()
        if 'data' in tx_dict and 'nft' in tx_dict['data']:
            nft_data = tx_dict['data']['nft']
            if 'timestamp' in nft_data and isinstance(nft_data['timestamp'], datetime):
                nft_data['timestamp'] = nft_data['timestamp'].isoformat()
        return tx_dict

    return app, socketio

if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)