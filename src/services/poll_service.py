import uuid
from datetime import datetime, timedelta

class PollService:
    """
    Lógica para crear encuestas, registrar votos, cierre y resultados.
    """
    def __init__(self, encuesta_repo, nft_service, observer=None, desempate_strategy=None):
        self.encuesta_repo = encuesta_repo
        self.nft_service = nft_service
        self.observer = observer
        self.desempate_strategy = desempate_strategy

    def _auto_close_polls(self):
        for encuesta in self.encuesta_repo.get_all():
            if encuesta.estado == "activa":
                fin = encuesta.timestamp_inicio + timedelta(seconds=encuesta.duracion_segundos)
                if datetime.now() >= fin:
                    self.close_poll(encuesta.id)

    def create_poll(self, pregunta, opciones, duracion_segundos, tipo):
        self._auto_close_polls()
        poll_id = str(uuid.uuid4())
        from src.models.encuesta import Encuesta
        encuesta = Encuesta(
            id=poll_id,
            pregunta=pregunta,
            opciones=opciones,
            duracion_segundos=duracion_segundos,
            tipo=tipo
        )
        self.encuesta_repo.save(encuesta)
        return poll_id

    def vote(self, poll_id, username, opcion):
        self._auto_close_polls()
        encuesta = self.encuesta_repo.get(poll_id)
        if not encuesta or encuesta.estado != "activa":
            raise ValueError("Encuesta no encontrada o no activa.")
        if any(v.usuario == username for v in encuesta.votos):
            raise ValueError("El usuario ya ha votado en esta encuesta.")
        from src.models.voto import Voto
        if encuesta.tipo == "multiple":
            if not isinstance(opcion, list):
                raise ValueError("Debe proporcionar una lista de opciones.")
            for op in opcion:
                encuesta.votos.append(Voto(username, op))
                self.nft_service.mint_token(username, poll_id, op)
        else:
            encuesta.votos.append(Voto(username, opcion))
            self.nft_service.mint_token(username, poll_id, opcion)
        self.encuesta_repo.save(encuesta)

    def close_poll(self, poll_id):
        encuesta = self.encuesta_repo.get(poll_id)
        if not encuesta or encuesta.estado != "activa":
            return
        encuesta.estado = "cerrada"
        self.encuesta_repo.save(encuesta)
        if self.observer:
            self.observer.notify("poll_closed", encuesta)

    def get_partial_results(self, poll_id):
        self._auto_close_polls()
        encuesta = self.encuesta_repo.get(poll_id)
        if not encuesta:
            return None
        total = len(encuesta.votos)
        conteo = {op: 0 for op in encuesta.opciones}
        for v in encuesta.votos:
            if isinstance(v.opcion, list):
                for op in v.opcion:
                    conteo[op] += 1
            else:
                conteo[v.opcion] += 1
        porcentajes = {op: (conteo[op] / total * 100 if total > 0 else 0) for op in conteo}
        return {"conteo": conteo, "porcentajes": porcentajes}

    def get_final_results(self, poll_id):
        encuesta = self.encuesta_repo.get(poll_id)
        if not encuesta or encuesta.estado != "cerrada":
            return None
        resultados = self.get_partial_results(poll_id)
        max_votos = max(resultados["conteo"].values()) if resultados["conteo"] else 0
        ganadores = [op for op, c in resultados["conteo"].items() if c == max_votos and max_votos > 0]
        if len(ganadores) > 1 and self.desempate_strategy:
            ganador = self.desempate_strategy.resolve(encuesta)
            resultados["desempate"] = ganador
        else:
            resultados["desempate"] = ganadores[0] if ganadores else None
        return resultados
