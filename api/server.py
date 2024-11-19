from flask import Flask
from flask_socketio import SocketIO
from api.routes.wallet_routes import wallet_routes
from api.routes.blockchain_routes import blockchain_routes
from api.routes.nft_routes import nft_routes
from api.routes.smart_contract_routes import smart_contract_routes

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)

    # Register the Blueprints
    app.register_blueprint(wallet_routes, url_prefix='/api/wallet')
    app.register_blueprint(blockchain_routes, url_prefix='/api/blockchain')
    app.register_blueprint(nft_routes, url_prefix='/api/nft')
    app.register_blueprint(smart_contract_routes, url_prefix='/api/contract')

    return app, socketio

if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)