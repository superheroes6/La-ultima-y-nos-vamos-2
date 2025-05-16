import uuid
from datetime import datetime
from src.models.token_nft import TokenNFT

class NFTService:
    """
    Generación y transferencia de tokens NFT.
    """
    def __init__(self, nft_repo):
        self.nft_repo = nft_repo

    def mint_token(self, username, poll_id, option):
        """
        Genera y almacena un nuevo token NFT tras un voto.
        """
        token_id = str(uuid.uuid4())
        issued_at = datetime.now()
        token = TokenNFT(
            token_id=token_id,
            owner=username,
            poll_id=poll_id,
            option=option,
            issued_at=issued_at
        )
        self.nft_repo.save(token)
        return token

    def get_tokens_by_user(self, username):
        """
        Devuelve todos los tokens NFT de un usuario.
        """
        return self.nft_repo.get_by_owner(username)

    def transfer_token(self, token_id, current_owner, new_owner):
        """
        Transfiere un token a otro usuario si el owner es correcto.
        """
        token = self.nft_repo.get(token_id)
        if not token:
            raise ValueError("Token no encontrado.")
        if token.owner != current_owner:
            raise PermissionError("No eres el propietario de este token.")
        token.owner = new_owner
        self.nft_repo.save(token)
        return token
