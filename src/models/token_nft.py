from datetime import datetime

class TokenNFT:
    """
    Representa el token coleccionable generado por un voto.
    """
    def __init__(self, token_id, owner, poll_id, option, issued_at: datetime):
        self.token_id = token_id
        self.owner = owner
        self.poll_id = poll_id
        self.option = option
        self.issued_at = issued_at
