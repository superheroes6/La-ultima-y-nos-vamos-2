class PresentacionStrategy:
    """
    Estrategia para presentar resultados.
    """
    def presentar(self, resultados):
        # Por defecto: texto simple
        return str(resultados)
