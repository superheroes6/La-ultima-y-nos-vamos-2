class CLIController:
    """
    Parseo de comandos del streamer y llamadas a servicios.
    """
    def __init__(self, poll_service, user_service, nft_service):
        self.poll_service = poll_service
        self.user_service = user_service
        self.nft_service = nft_service

    def crear_encuesta(self, pregunta, opciones, duracion, tipo):
        return self.poll_service.create_poll(pregunta, opciones, duracion, tipo)

    def votar(self, poll_id, username, opcion):
        return self.poll_service.vote(poll_id, username, opcion)

    def cerrar_encuesta(self, poll_id):
        self.poll_service.close_poll(poll_id)

    def ver_resultados(self, poll_id):
        return self.poll_service.get_partial_results(poll_id)

    def mis_tokens(self, username):
        return self.nft_service.get_tokens_by_user(username)

    def transferir_token(self, token_id, current_owner, new_owner):
        return self.nft_service.transfer_token(token_id, current_owner, new_owner)
