from transformers import pipeline

class ChatbotService:
    """
    Encapsula el pipeline de Hugging Face y lógica de respuesta.
    """
    def __init__(self, poll_service=None):
        # Usa solo pipeline, elimina Conversation
        self.chatbot = pipeline("text-generation", model="gpt2")
        self.poll_service = poll_service
        self.historial = {}  # username -> list of (user_msg, bot_msg)

    def chatbot_response(self, username, message):
        """
        Responde a la pregunta del usuario, usando lógica contextual o IA.
        """
        # Palabras clave para respuestas contextuales
        keywords = ["quién va ganando", "quien va ganando", "cuánto falta", "cuanto falta", "resultado", "ganador", "encuesta"]
        msg_lower = message.lower()
        if any(k in msg_lower for k in keywords) and self.poll_service:
            # Ejemplo simple: muestra resultados de la última encuesta activa
            encuestas = self.poll_service.encuesta_repo.get_all()
            activas = [e for e in encuestas if e.estado == "activa"]
            if activas:
                poll = activas[-1]
                parciales = self.poll_service.get_partial_results(poll.id)
                respuesta = f"Resultados parciales de '{poll.pregunta}':\n"
                for op, c in parciales["conteo"].items():
                    respuesta += f"- {op}: {c} votos ({parciales['porcentajes'][op]:.1f}%)\n"
            else:
                respuesta = "No hay encuestas activas en este momento."
        else:
            # Usa text-generation en vez de conversational
            output = self.chatbot(message, max_length=60, num_return_sequences=1)
            respuesta = output[0]['generated_text']
        # Guardar historial (opcional)
        if username not in self.historial:
            self.historial[username] = []
        self.historial[username].append((message, respuesta))
        return respuesta

    # Métodos principales
    # ...existing code...
