import hashlib
import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA256


class Wallet:
    def __init__(self):
        """
        Inicializa una billetera generando claves privada y pública.
        """
        self.private_key = self._generate_private_key()
        self.public_key = self.private_key.public_key()
        self.address = self._generate_address()

    @staticmethod
    def _generate_private_key():
        """
        Genera una clave privada RSA.
        """
        return rsa.generate_private_key(public_exponent=65537, key_size=2048)

    def _generate_address(self) -> str:
        """
        Genera una dirección de billetera basada en el hash de la clave pública.
        """
        pubkey_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return hashlib.sha256(pubkey_bytes).hexdigest()[:40]  # Usamos un hash truncado como dirección.

    def sign_message(self, message: str) -> str:
        """
        Firma un mensaje utilizando la clave privada.
        """
        signature = self.private_key.sign(
            message.encode(),
            PKCS1v15(),
            SHA256(),
        )
        return base64.b64encode(signature).decode()

    def export_private_key(self, filepath: str):
        """
        Exporta la clave privada a un archivo.
        """
        with open(filepath, "wb") as file:
            file.write(
                self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )

    def export_public_key(self, filepath: str):
        """
        Exporta la clave pública a un archivo.
        """
        with open(filepath, "wb") as file:
            file.write(
                self.public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

    @staticmethod
    def load_private_key(filepath: str):
        """
        Carga una clave privada desde un archivo.
        """
        with open(filepath, "rb") as file:
            private_key = serialization.load_pem_private_key(
                file.read(),
                password=None,
            )
        return private_key

    def __repr__(self):
        return f"Wallet(address={self.address})"
