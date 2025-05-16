class Usuario:
    """
    Identifica a cada espectador registrado.
    """
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.tokens = []
