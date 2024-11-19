from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from api.routes.wallet_routes import wallet_routes
from api.routes.blockchain_routes import create_blockchain_routes
from api.routes.nft_routes import create_nft_routes
from api.routes.smart_contract_routes import smart_contract_routes
from blockchain.core.blockchain import Blockchain

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
    def handle_connect():
        emit('blockchain_update', {'blocks': [block.__dict__ for block in julinks.chain]})

    @socketio.on('request_blockchain')
    def handle_request_blockchain():
        emit('blockchain_update', {'blocks': [block.__dict__ for block in julinks.chain]})

    @socketio.on('mine_block')
    def handle_mine_block():
        julinks.mine_pending_transactions()
        emit('blockchain_update', {'blocks': [block.__dict__ for block in julinks.chain]}, broadcast=True)

    return app, socketio

if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)