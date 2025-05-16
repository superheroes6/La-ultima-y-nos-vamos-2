class UIController:
    """
    Controlador para la interfaz Gradio.
    """
    def __init__(self, poll_service, chatbot_service, nft_service):
        self.poll_service = poll_service
        self.chatbot_service = chatbot_service
        self.nft_service = nft_service
    # Métodos principales
