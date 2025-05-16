from src.models.usuario import Usuario

class UsuarioRepository:
    """
    Gestiona credenciales y datos de usuarios.
    """
    def __init__(self):
        self.usuarios = {}

    def exists(self, username):
        return username in self.usuarios

    def save(self, username, password_hash):
        self.usuarios[username] = Usuario(username, password_hash)

    def get(self, username):
        return self.usuarios.get(username)
