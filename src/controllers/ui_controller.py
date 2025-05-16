class UIController:
    """
    Controlador para la interfaz Gradio.
    """
    def __init__(self, poll_service, chatbot_service, nft_service):
        self.poll_service = poll_service
        self.chatbot_service = chatbot_service
        self.nft_service = nft_service

    def get_active_polls(self):
        return [e for e in self.poll_service.encuesta_repo.get_all() if e.estado == "activa"]

    def votar(self, poll_id, username, opcion):
        return self.poll_service.vote(poll_id, username, opcion)

    def chatbot(self, username, message):
        return self.chatbot_service.chatbot_response(username, message)

    def get_tokens(self, username):
        return self.nft_service.get_tokens_by_user(username)

    def transferir_token(self, token_id, current_owner, new_owner):
        return self.nft_service.transfer_token(token_id, current_owner, new_owner)
