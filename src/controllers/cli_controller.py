class CLIController:
    """
    Parseo de comandos del streamer y llamadas a servicios.
    """
    def __init__(self, poll_service, user_service, nft_service):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service
    # Métodos principales
