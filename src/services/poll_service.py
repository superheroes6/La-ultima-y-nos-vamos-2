class PollService:
    """
    Lógica para crear encuestas, registrar votos, cierre y resultados.
    """
    def __init__(self, encuesta_repo, nft_service):
        self.encuesta_repo = encuesta_repo
        self.nft_service = nft_service
    # Métodos principales
