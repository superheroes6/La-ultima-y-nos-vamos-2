# La última y nos vamos 2

## Introducción y contexto

En el entorno actual del entretenimiento digital, el streaming ha evolucionado más allá de la simple difusión de partidas de videojuegos o eventos en vivo: los creadores de contenido buscan constantemente nuevas formas de involucrar a su audiencia, ofrecer experiencias interactivas y premiar la fidelidad de sus seguidores. Al mismo tiempo, avances en inteligencia artificial conversacional y la emergente cultura de tokens no fungibles (NFTs) abren la puerta a construir plataformas que combinen votaciones en tiempo real, chatbots capaces de conversar de manera natural y economía digital simulada mediante coleccionables.

Con este escenario como telón de fondo, se plantea el desarrollo de una aplicación de votaciones interactivas para streamers —tanto mediante línea de comandos (CLI) para la administración del canal como con una interfaz web ligera (usando Gradio) para la audiencia— que incorpore tres módulos principales:

- **Sistema de encuestas en vivo:** crea, administra y cierra encuestas con tiempo limitado, permitiendo a los espectadores votar en tiempo real.
- **Chatbot IA:** integra un modelo preentrenado de Hugging Face Transformers para responder preguntas de los espectadores sobre las encuestas, el stream y cualquier tema relevante.
- **Tokens NFT simulados:** cada voto emitido genera un “token coleccionable” único, que los usuarios podrán ver en una galería y transferir entre sí.

El objetivo de este ejercicio es que el alumno ponga en práctica conceptos avanzados de Programación Orientada a Objetos (POO), patrones de diseño (Observer, Factory, Strategy, etc.), arquitectura modular y buenas prácticas de ingeniería de software (persistencia desacoplada, pruebas unitarias, documentación), al tiempo que construye una plataforma atractiva y moderna.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

- Modo CLI:
  ```bash
  python src/app.py
  ```
- Modo UI:
  ```bash
  python src/app.py --ui
  ```

## Estructura de proyecto y configuración

```
la_ultima_y_nos_vamos/
├── src/
│   ├── app.py            # Punto de entrada
│   ├── config.py         # Carga de parámetros (JSON/YAML)
│   ├── models/
│   │   ├── encuesta.py
│   │   ├── voto.py
│   │   ├── usuario.py
│   │   └── token_nft.py
│   ├── repositories/
│   │   ├── encuesta_repo.py
│   │   ├── usuario_repo.py
│   │   └── nft_repo.py
│   ├── services/
│   │   ├── poll_service.py
│   │   ├── user_service.py
│   │   ├── nft_service.py
│   │   └── chatbot_service.py
│   ├── patterns/
│   │   ├── observer.py
│   │   ├── factory.py
│   │   └── strategy.py
│   ├── controllers/
│   │   ├── cli_controller.py
│   │   └── ui_controller.py
│   └── ui/
│       └── gradio_app.py
├── tests/
│   ├── test_models.py
│   ├── test_repositories.py
│   ├── test_services.py
│   ├── test_patterns.py
│   └── test_cli.py
├── requirements.txt
└── README.md
```

### requirements.txt

```
gradio
transformers
pytest
bcrypt
```

## Descripción

Plataforma de votaciones interactivas para streamers con encuestas, chatbot IA y tokens NFT simulados.

---

## Objetivos de aprendizaje

Al completar este proyecto, el estudiante demostrará su capacidad para:

- Diseñar sistemas complejos empleando principios SOLID y patrones de diseño.
- Integrar tecnologías heterogéneas: CLI, Gradio (UI), Transformers (IA conversacional) y simulación de NFTs.
- Gestionar persistencia de datos de forma desacoplada, ya sea con archivos JSON o SQLite.
- Escribir pruebas unitarias con pytest que aseguren la fiabilidad de cada componente.
- Documentar y estructurar un proyecto de software de tamaño medio de manera profesional.

---

## Arquitectura general y módulos

La arquitectura del proyecto está dividida en las siguientes capas y módulos:

### Modelos de dominio (`src/models/`)
- **Encuesta (Poll):** representa una encuesta con id, pregunta, opciones, votos, estado (activa/cerrada), timestamps y duración.
- **Voto (Vote):** asocia un usuario con una opción en una encuesta.
- **TokenNFT:** representa el token coleccionable, con id único, metadatos (encuesta, opción, fecha, propietario).
- **Usuario (User):** identifica a cada espectador registrado (username, password hash, lista de tokens).

### Repositorios (`src/repositories/`)
- **EncuestaRepository:** leer/escribir encuestas y votos en JSON o SQLite.
- **UsuarioRepository:** gestionar credenciales y datos de usuarios.
- **NFTRepository:** almacenar y consultar tokens NFT.

### Servicios de negocio (`src/services/`)
- **PollService:** lógica para crear encuestas, registrar votos (un voto por usuario), cierre automático/manual, cálculo de resultados y desempates.
- **UserService:** registro, login y verificación de permisos para votar.
- **NFTService:** generación de tokens al votar, transferencia entre usuarios.
- **ChatbotService:** encapsula el pipeline de Hugging Face y la lógica de respuesta, incluyendo consultas al estado de las encuestas.

### Patrones de diseño (`src/patterns/`)
- **Observer:** notifica a NFTService, UIController y ChatbotService cuando una encuesta se cierra.
- **Factory Method:** crea instancias de distintos tipos de Encuesta (p.ej. simple, múltiple, ponderada) o de TokenNFT (p.ej. estándar, edición limitada).
- **Strategy:** encapsula algoritmos de desempate (alfabético, aleatorio, prórroga) y formatos de presentación de resultados (texto, gráfico ASCII, JSON).

### Controladores e interfaces (`src/controllers/` y `src/ui/`)
- **CLI Controller:** parsea comandos del streamer (crear_encuesta, listar_encuestas, cerrar_encuesta, ver_resultados, etc.) y llama a los servicios.
- **Gradio UI:**
  - Sección Encuestas: muestra encuestas activas y formulario para votar.
  - Sección Chatbot: cuadro de diálogo para interactuar con el modelo.
  - Sección Tokens: galería de tokens del usuario con opción de transferir a otro username.

### Punto de entrada (`app.py` o `main.py`)
- Inicializa configuración (puerto, rutas, parámetros de IA, estrategias).
- Arranca la interactividad: por defecto lanza la CLI; si se ejecuta con `--ui`, inicia el servidor Gradio en paralelo.

---

## Requisitos funcionales detallados

### 4.1 Registro y autenticación de usuarios

**Registro (`UserService.register`):**
- Solicita username y password.
- Valida que el nombre no exista (único).
- Almacena el password_hash (usando `hashlib.pbkdf2_hmac` o `bcrypt`).

**Login (`UserService.login`):**
- Verifica credenciales.
- Retorna un token de sesión (puede ser un string UUID) o marca al usuario como «logueado» en la sesión CLI.

**Persistencia:**
- Las credenciales y la sesión no persisten más allá del reinicio (a menos que implementes «recordarme», opcional).

### 4.2 Gestión de encuestas

**Crear encuesta (`PollService.create_poll`):**
- Parámetros: `pregunta: str`, `opciones: List[str]`, `duracion_segundos: int`, `tipo: str` (simple/multiple).
- Asigna un id secuencial o UUID, `timestamp_inicio = ahora`, `estado = activa`.

**Votar (`PollService.vote`):**
- Parámetros: `poll_id`, `username`, `opcion` (o lista de opciones si es múltiple).
- Verifica que la encuesta existe y está activa, y que el usuario no haya votado ya.
- Registra el voto en `VotoRepository` o directamente en el objeto encuesta.
- Genera un token NFT asociando `username`, `poll_id`, `opcion`, `timestamp`.

**Cierre automático:**
- El servicio debe comprobar antes de cada operación (o mediante un mecanismo interno) si alguna encuesta ha superado su `timestamp_inicio + duracion` y, de ser así, invocar `close_poll(poll_id)`.
- Al cerrar: cambiar `estado = cerrada`, notificar observadores (Observer) y almacenar resultado.

**Cierre manual:**
- Comando CLI `cerrar_encuesta <poll_id>` permite al streamer cerrar anticipadamente.

**Resultados:**
- Parciales: método `get_partial_results(poll_id)` retorna conteo y porcentaje por opción.
- Finales: `get_final_results(poll_id)` hace lo mismo tras cierre.
- Desempate: si hay empate, invocar `DesempateStrategy.resolve(encuesta)`.
