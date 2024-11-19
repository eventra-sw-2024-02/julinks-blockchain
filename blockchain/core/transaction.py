import hashlib
import json
from typing import Optional


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float, data: Optional[dict] = None, signature: Optional[str] = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.data = data if data else {}
        self.signature = signature  # La firma será añadida posteriormente

    def to_dict(self) -> dict:
        """
        Representa la transacción como un diccionario, excluyendo la firma.
        """
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "data": self.data,
        }

    def compute_hash(self) -> str:
        """
        Calcula el hash de la transacción.
        """
        transaction_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def sign_transaction(self, private_key: str):
        """
        Firma la transacción utilizando una clave privada (simplificada para este caso).
        """
        if not private_key:
            raise ValueError("Se requiere una clave privada para firmar la transacción.")
        self.signature = hashlib.sha256((private_key + self.compute_hash()).encode()).hexdigest()

    def is_valid(self) -> bool:
        """
        Verifica si la transacción es válida (firma presente).
        """
        return self.signature is not None

    def __repr__(self):
        return f"Transaction(sender={self.sender}, receiver={self.receiver}, amount={self.amount}, data={self.data})"