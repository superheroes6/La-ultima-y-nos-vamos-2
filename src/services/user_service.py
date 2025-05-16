import bcrypt
import uuid

class UserService:
    """
    Registro, login y verificación de permisos para votar.
    """
    def __init__(self, usuario_repo):
        self.usuario_repo = usuario_repo
        self.sesiones = {}  # username -> session_token

    def register(self, username, password):
        if self.usuario_repo.exists(username):
            raise ValueError("El nombre de usuario ya existe.")
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.usuario_repo.save(username, password_hash)
        return True

    def login(self, username, password):
        user = self.usuario_repo.get(username)
        if not user:
            return None
        if bcrypt.checkpw(password.encode(), user.password_hash):
            token = str(uuid.uuid4())
            self.sesiones[username] = token
            return token
        return None

    def is_logged_in(self, username, token):
        return self.sesiones.get(username) == token

    # Métodos principales
    # ...existing code...
