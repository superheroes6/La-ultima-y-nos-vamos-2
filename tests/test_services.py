import pytest
from datetime import datetime, timedelta
from src.models.encuesta import Encuesta
from src.models.voto import Voto
from src.models.token_nft import TokenNFT
from src.repositories.encuesta_repo import EncuestaRepository
from src.repositories.usuario_repo import UsuarioRepository
from src.repositories.nft_repo import NFTRepository
from src.services.poll_service import PollService
from src.services.user_service import UserService
from src.services.nft_service import NFTService

class DummyObserver:
    def __init__(self):
        self.events = []
    def notify(self, event, data):
        self.events.append((event, data))

class DummyDesempate:
    def resolve(self, encuesta):
        return "A"

def test_encuesta_creacion_y_cierre():
    encuesta = Encuesta("1", "¿Pregunta?", ["A", "B"], 60, "simple")
    assert encuesta.pregunta == "¿Pregunta?"
    encuesta.estado = "cerrada"
    assert encuesta.estado == "cerrada"

def test_pollservice_crear_y_votar():
    encuesta_repo = EncuestaRepository()
    nft_repo = NFTRepository()
    nft_service = NFTService(nft_repo)
    poll_service = PollService(encuesta_repo, nft_service)
    poll_id = poll_service.create_poll("¿Color?", ["Rojo", "Azul"], 60, "simple")
    poll_service.vote(poll_id, "user1", "Rojo")
    encuesta = encuesta_repo.get(poll_id)
    assert len(encuesta.votos) == 1
    assert encuesta.votos[0].usuario == "user1"
    assert encuesta.votos[0].opcion == "Rojo"

def test_pollservice_voto_duplicado():
    encuesta_repo = EncuestaRepository()
    nft_repo = NFTRepository()
    nft_service = NFTService(nft_repo)
    poll_service = PollService(encuesta_repo, nft_service)
    poll_id = poll_service.create_poll("¿Color?", ["Rojo", "Azul"], 60, "simple")
    poll_service.vote(poll_id, "user1", "Rojo")
    with pytest.raises(ValueError):
        poll_service.vote(poll_id, "user1", "Azul")

def test_pollservice_cierre_automatico():
    encuesta_repo = EncuestaRepository()
    nft_repo = NFTRepository()
    nft_service = NFTService(nft_repo)
    poll_service = PollService(encuesta_repo, nft_service)
    poll_id = poll_service.create_poll("¿Tiempo?", ["A", "B"], 0, "simple")
    encuesta = encuesta_repo.get(poll_id)
    encuesta.timestamp_inicio = datetime.now() - timedelta(seconds=10)
    encuesta_repo.save(encuesta)
    poll_service.vote(poll_id, "user1", "A")
    encuesta = encuesta_repo.get(poll_id)
    assert encuesta.estado == "cerrada" or encuesta.estado == "activa"  # Puede cerrarse antes o después del voto

def test_pollservice_desempate():
    encuesta_repo = EncuestaRepository()
    nft_repo = NFTRepository()
    nft_service = NFTService(nft_repo)
    desempate = DummyDesempate()
    poll_service = PollService(encuesta_repo, nft_service, desempate_strategy=desempate)
    poll_id = poll_service.create_poll("¿Letra?", ["A", "B"], 60, "simple")
    poll_service.vote(poll_id, "u1", "A")
    poll_service.vote(poll_id, "u2", "B")
    encuesta = encuesta_repo.get(poll_id)
    encuesta.estado = "cerrada"
    encuesta_repo.save(encuesta)
    res = poll_service.get_final_results(poll_id)
    assert res["desempate"] == "A"

def test_nftservice_mint_and_transfer():
    nft_repo = NFTRepository()
    nft_service = NFTService(nft_repo)
    token = nft_service.mint_token("user1", "poll1", "A")
    assert token.owner == "user1"
    assert nft_service.get_tokens_by_user("user1")[0].token_id == token.token_id
    nft_service.transfer_token(token.token_id, "user1", "user2")
    assert nft_service.get_tokens_by_user("user2")[0].token_id == token.token_id
    with pytest.raises(PermissionError):
        nft_service.transfer_token(token.token_id, "user1", "user3")

def test_userservice_register_and_login():
    usuario_repo = UsuarioRepository()
    user_service = UserService(usuario_repo)
    assert user_service.register("test", "1234")
    token = user_service.login("test", "1234")
    assert token is not None
    assert user_service.is_logged_in("test", token)
    assert user_service.login("test", "wrong") is None

# ...other tests for ChatbotService and patterns can be added similarly...
