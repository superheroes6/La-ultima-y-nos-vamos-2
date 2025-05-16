from src.models.token_nft import TokenNFT

class TokenNFTFactory:
    """
    Crea instancias de distintos tipos de TokenNFT.
    """
    @staticmethod
    def crear_token(tipo, *args, **kwargs):
        # Aquí puedes extender para otros tipos
        return TokenNFT(*args, **kwargs)
