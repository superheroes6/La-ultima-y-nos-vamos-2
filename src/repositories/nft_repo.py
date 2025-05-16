class NFTRepository:
    """
    Almacena y consulta tokens NFT.
    """
    def __init__(self):
        self.tokens = {}

    def save(self, token):
        self.tokens[token.token_id] = token

    def get(self, token_id):
        return self.tokens.get(token_id)

    def get_by_owner(self, owner):
        return [t for t in self.tokens.values() if t.owner == owner]
