from src.models.encuesta import Encuesta

class EncuestaFactory:
    """
    Crea instancias de distintos tipos de Encuesta.
    """
    @staticmethod
    def crear_encuesta(tipo, *args, **kwargs):
        # Aquí puedes extender para otros tipos
        return Encuesta(*args, **kwargs)
