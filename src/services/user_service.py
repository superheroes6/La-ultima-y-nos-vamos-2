class UserService:
    """
    Registro, login y verificación de permisos para votar.
    """
    def __init__(self, usuario_repo):
        self.usuario_repo = usuario_repo
    # Métodos principales
