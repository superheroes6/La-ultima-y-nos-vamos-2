class DesempateStrategy:
    """
    Estrategia para resolver empates.
    """
    def resolve(self, encuesta):
        # Por defecto: desempate alfabético
        opciones = [v.opcion for v in encuesta.votos]
        if opciones:
            return sorted(set(opciones))[0]
        return None
