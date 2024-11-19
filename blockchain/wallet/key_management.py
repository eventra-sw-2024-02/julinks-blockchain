from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
import base64


def verify_signature(public_key_pem: bytes, message: str, signature: str) -> bool:
    """
    Verifica la firma de un mensaje usando la clave pública.
    """
    public_key = serialization.load_pem_public_key(public_key_pem)
    try:
        public_key.verify(
            base64.b64decode(signature),
            message.encode(),
            PKCS1v15(),
            SHA256(),
        )
        return True
    except Exception:
        return False
