class Marketplace:
    def __init__(self):
        self.listings = []  # NFTs disponibles para la venta

    def list_nft(self, nft, price):
        """
        Lista un NFT en el mercado.
        """
        self.listings.append({"nft": nft, "price": price})

    def buy_nft(self, nft_id, buyer):
        """
        Permite que un comprador adquiera un NFT listado.
        """
        for listing in self.listings:
            if listing["nft"].id == nft_id:
                nft = listing["nft"]
                nft.transfer(buyer)  # Transfiere la propiedad al comprador
                self.listings.remove(listing)  # Remueve el NFT del mercado
                return nft
        raise ValueError("NFT no encontrado en las listas del mercado.")
