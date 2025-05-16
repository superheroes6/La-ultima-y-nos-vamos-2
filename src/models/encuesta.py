from typing import List
from datetime import datetime

class Encuesta:
    """
    Representa una encuesta con pregunta, opciones, votos y estado.
    """
    def __init__(self, id, pregunta, opciones: List[str], duracion_segundos: int, tipo: str):
        self.id = id
        self.pregunta = pregunta
        self.opciones = opciones
        self.duracion_segundos = duracion_segundos
        self.tipo = tipo  # "simple" o "multiple"
        self.estado = "activa"
        self.timestamp_inicio = datetime.now()
        self.votos = []  # Lista de Voto
