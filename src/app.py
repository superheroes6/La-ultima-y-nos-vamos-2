import sys

from src.repositories.encuesta_repo import EncuestaRepository
from src.repositories.usuario_repo import UsuarioRepository
from src.repositories.nft_repo import NFTRepository
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService
from src.services.chatbot_service import ChatbotService
from src.controllers.cli_controller import CLIController
from src.controllers.ui_controller import UIController
from src.ui.gradio_app import launch_gradio_app

def main():
    """
    Inicializa la configuración y lanza CLI o UI.
    """
    # Inicialización de repositorios y servicios
    encuesta_repo = EncuestaRepository()
    usuario_repo = UsuarioRepository()
    nft_repo = NFTRepository()
    nft_service = NFTService(nft_repo)
    user_service = UserService(usuario_repo)
    poll_service = PollService(encuesta_repo, nft_service)
    chatbot_service = ChatbotService(poll_service=poll_service)

    # Controladores
    cli_controller = CLIController(poll_service, user_service, nft_service)
    ui_controller = UIController(poll_service, chatbot_service, nft_service)

    # Selección de modo
    if "--ui" in sys.argv:
        launch_gradio_app(ui_controller)
    else:
        # CLI loop simple de ejemplo
        print("Bienvenido a la CLI de votaciones. Escribe 'salir' para terminar.")
        while True:
            cmd = input(">> ")
            if cmd.strip() == "salir":
                break
            # Aquí deberías parsear y ejecutar comandos usando cli_controller
            print("Comando recibido:", cmd)

if __name__ == "__main__":
    main()
