from typing import List, Dict
from datetime import datetime

class Encuesta:
    """
    Representa una encuesta con pregunta, opciones, votos y estado.
    """
    def __init__(self, id, pregunta, opciones, duracion_segundos, tipo):
        self.id = id
        self.pregunta = pregunta
        self.opciones = opciones
        self.duracion_segundos = duracion_segundos
        self.tipo = tipo
        self.estado = "activa"
        self.timestamp_inicio = datetime.now()
        self.votos = []
