import gradio as gr

def launch_gradio_app(ui_controller):
    """
    Lanza la interfaz Gradio y muestra el enlace de acceso.
    """
    def votar_fn(poll_id, username, opcion):
        try:
            # Permitir opciones múltiples separadas por coma
            if "," in opcion:
                opcion = [o.strip() for o in opcion.split(",")]
            ui_controller.votar(poll_id, username, opcion)
            return "Voto registrado"
        except Exception as e:
            return str(e)

    def chatbot_fn(username, message):
        return ui_controller.chatbot(username, message)

    def tokens_fn(username):
        tokens = ui_controller.get_tokens(username)
        return "\n".join([f"{t.token_id} - {t.option} ({t.poll_id})" for t in tokens])

    def crear_encuesta_fn(pregunta, opciones, duracion, tipo):
        try:
            opciones_list = [o.strip() for o in opciones.split(",")]
            poll_id = ui_controller.poll_service.create_poll(pregunta, opciones_list, int(duracion), tipo)
            return f"Encuesta creada con id: {poll_id}"
        except Exception as e:
            return str(e)

    with gr.Blocks() as demo:
        gr.Markdown("# Encuestas en vivo")
        with gr.Tab("Crear Encuesta"):
            pregunta = gr.Textbox(label="Pregunta")
            opciones = gr.Textbox(label="Opciones (separadas por coma)")
            duracion = gr.Number(label="Duración (segundos)", value=60)
            tipo = gr.Dropdown(choices=["simple", "multiple"], label="Tipo", value="simple")
            crear_btn = gr.Button("Crear Encuesta")
            crear_out = gr.Textbox(label="Resultado")
            crear_btn.click(crear_encuesta_fn, [pregunta, opciones, duracion, tipo], crear_out)
        with gr.Tab("Encuestas"):
            poll_id = gr.Textbox(label="ID Encuesta")
            username = gr.Textbox(label="Usuario")
            opcion = gr.Textbox(label="Opción (o varias separadas por coma)")
            votar_btn = gr.Button("Votar")
            votar_out = gr.Textbox(label="Resultado")
            votar_btn.click(votar_fn, [poll_id, username, opcion], votar_out)
        with gr.Tab("Chatbot"):
            chat_username = gr.Textbox(label="Usuario")
            chat_input = gr.Textbox(label="Mensaje")
            chat_btn = gr.Button("Enviar")
            chat_out = gr.Textbox(label="Respuesta")
            chat_btn.click(chatbot_fn, [chat_username, chat_input], chat_out)
        with gr.Tab("Tokens"):
            tokens_username = gr.Textbox(label="Usuario")
            tokens_btn = gr.Button("Ver mis tokens")
            tokens_out = gr.Textbox(label="Tokens")
            tokens_btn.click(tokens_fn, [tokens_username], tokens_out)
    # Lanza Gradio y muestra el enlace en consola
    url = demo.launch(share=True)
    print(f"Accede a la interfaz web de Gradio aquí: {url}")
