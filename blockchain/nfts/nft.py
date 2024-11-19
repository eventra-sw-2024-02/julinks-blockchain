import uuid
from datetime import datetime

class NFT:
    def __init__(self, name, creator, metadata, owner=None):
        self.id = str(uuid.uuid4())  # ID único para cada NFT
        self.name = name
        self.creator = creator  # Dirección del creador
        self.owner = owner if owner else creator  # Por defecto, el creador es el propietario inicial
        self.metadata = metadata  # Metadatos (e.g., enlace a imagen, descripción)
        self.timestamp = datetime.now()  # Marca de tiempo de creación

    def transfer(self, new_owner):
        """
        Transfiere el NFT a un nuevo propietario.
        """
        self.owner = new_owner

    def __repr__(self):
        return (f"NFT(id={self.id}, name={self.name}, creator={self.creator}, "
                f"owner={self.owner}, metadata={self.metadata})")
