from .wallet_routes import wallet_routes
from .blockchain_routes import create_blockchain_routes
from .nft_routes import create_nft_routes
from .smart_contract_routes import smart_contract_routes

__all__ = ["wallet_routes", "create_blockchain_routes", "create_nft_routes", "smart_contract_routes"]