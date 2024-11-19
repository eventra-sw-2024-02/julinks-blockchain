import pytest
from datetime import datetime
from blockchain.nfts.nft import NFT

def test_nft_creation():
    name = "Test NFT"
    creator = "creator_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata)

    assert nft.name == name
    assert nft.creator == creator
    assert nft.owner == creator
    assert nft.metadata == metadata
    assert isinstance(nft.id, str)
    assert isinstance(nft.timestamp, datetime)

def test_nft_transfer():
    name = "Test NFT"
    creator = "creator_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata)

    new_owner = "new_owner_address"
    nft.transfer(new_owner)

    assert nft.owner == new_owner

def test_nft_to_dict():
    name = "Test NFT"
    creator = "creator_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata)

    nft_dict = nft.to_dict()

    assert nft_dict["id"] == nft.id
    assert nft_dict["name"] == nft.name
    assert nft_dict["creator"] == nft.creator
    assert nft_dict["owner"] == nft.owner
    assert nft_dict["metadata"] == nft.metadata
    assert nft_dict["timestamp"] == nft.timestamp.isoformat()

def test_nft_creation_with_owner():
    name = "Test NFT"
    creator = "creator_address"
    owner = "owner_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata, owner)

    assert nft.name == name
    assert nft.creator == creator
    assert nft.owner == owner
    assert nft.metadata == metadata
    assert isinstance(nft.id, str)
    assert isinstance(nft.timestamp, datetime)

def test_nft_transfer_to_same_owner():
    name = "Test NFT"
    creator = "creator_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata)

    nft.transfer(creator)

    assert nft.owner == creator

def test_nft_metadata_update():
    name = "Test NFT"
    creator = "creator_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata)

    new_metadata = {"image": "http://example.com/new_image.png", "description": "Updated description"}
    nft.metadata = new_metadata

    assert nft.metadata == new_metadata

def test_nft_repr():
    name = "Test NFT"
    creator = "creator_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata)

    expected_repr = (f"NFT(id={nft.id}, name={nft.name}, creator={nft.creator}, "
                     f"owner={nft.owner}, metadata={nft.metadata})")
    assert repr(nft) == expected_repr

def test_nft_invalid_metadata():
    name = "Test NFT"
    creator = "creator_address"
    metadata = "Invalid metadata"  # Metadata should be a dictionary

    with pytest.raises(TypeError):
        NFT(name, creator, metadata)

def test_nft_to_dict():
    name = "Test NFT"
    creator = "creator_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata)

    nft_dict = nft.to_dict()

    assert nft_dict["id"] == nft.id
    assert nft_dict["name"] == nft.name
    assert nft_dict["creator"] == nft.creator
    assert nft_dict["owner"] == nft.owner
    assert nft_dict["metadata"] == nft.metadata
    assert nft_dict["timestamp"] == nft.timestamp.isoformat()

def test_nft_creation_with_owner():
    name = "Test NFT"
    creator = "creator_address"
    owner = "owner_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata, owner)

    assert nft.name == name
    assert nft.creator == creator
    assert nft.owner == owner
    assert nft.metadata == metadata
    assert isinstance(nft.id, str)
    assert isinstance(nft.timestamp, datetime)

def test_nft_transfer_to_same_owner():
    name = "Test NFT"
    creator = "creator_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata)

    nft.transfer(creator)

    assert nft.owner == creator

def test_nft_metadata_update():
    name = "Test NFT"
    creator = "creator_address"
    metadata = {"image": "http://example.com/image.png", "description": "Test description"}
    nft = NFT(name, creator, metadata)

    new_metadata = {"image": "http://example.com/new_image.png", "description": "Updated description"}
    nft.metadata = new_metadata

    assert nft.metadata == new_metadata