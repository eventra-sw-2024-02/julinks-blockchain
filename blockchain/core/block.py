import hashlib
import time


class Block:
    def __init__(self, index: int, timestamp: str, data: str, previous_hash: str, nonce: int = None, hash: str = None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce if nonce is not None else 0
        self.hash = hash if hash is not None else self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calcula el hash del bloque utilizando SHA256.
        """
        block_data = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash}, previous_hash={self.previous_hash}, data={self.data})"
