class EncuestaRepository:
    """
    Permite leer y escribir encuestas y votos.
    """
    def __init__(self):
        self.encuestas = {}

    def save(self, encuesta):
        self.encuestas[encuesta.id] = encuesta

    def get(self, encuesta_id):
        return self.encuestas.get(encuesta_id)

    def get_all(self):
        return list(self.encuestas.values())
