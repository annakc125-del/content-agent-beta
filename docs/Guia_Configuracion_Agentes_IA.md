# Guía Paso a Paso: Configuración del Ecosistema de Agentes IA (Beta)

**Autor:** Manus AI
**Fecha:** Abril 2026

Esta guía detallada está diseñada para principiantes y explica paso a paso cómo configurar el Ecosistema de Agentes de Inteligencia Artificial para la creación de contenido multimedia, basado en el repositorio `content-agent-beta`.

El sistema utiliza tres agentes principales: un Orquestador (selecciona clips), un Creador de Narrativa (escribe guiones y copy) y un Productor Multimedia (corta el video y añade subtítulos). Para que todo funcione, es necesario conectar varias plataformas externas.

A continuación, se detalla qué partes del proceso están automatizadas por el código (y puedo hacer por ti) y qué partes requieren configuración manual por tu parte.

---

## 1. División de Responsabilidades

Para entender mejor el proceso, aquí tienes una tabla que separa lo que el código (y yo como asistente) podemos hacer automáticamente, y lo que tú debes configurar manualmente por razones de seguridad y privacidad.

| Componente / Tarea | ¿Qué hace Manus / El Código? | ¿Qué debes hacer tú manualmente? |
| :--- | :--- | :--- |
| **Repositorio y Código** | Clonar el repositorio, explorar archivos, explicar el código y ejecutar los scripts de Python localmente. | Instalar Python y FFmpeg en tu computadora si deseas ejecutarlo localmente. |
| **OpenAI (Inteligencia Artificial)** | El código se conecta automáticamente a la API, envía los prompts y procesa las respuestas JSON. | Crear la cuenta en OpenAI, añadir un método de pago y generar la API Key secreta [1]. |
| **Automatización (n8n / Make)** | Proveer la lógica de cómo estructurar el flujo de trabajo (webhook -> transcripción -> agentes). | Crear la cuenta en n8n o Make.com y configurar visualmente los nodos conectando tus cuentas [2]. |
| **Almacenamiento (Google Drive)** | El código lee archivos locales y guarda los resultados en la carpeta `output/`. | Crear las carpetas en Google Drive y conectarlas a n8n/Make para subir y descargar videos. |
| **Formularios (Typeform / Tally)** | Sugerir la estructura de preguntas para el formulario de entrada de clientes. | Crear el formulario y configurar el webhook que envía los datos a n8n/Make [3]. |

---

## 2. Configuración Manual Paso a Paso (Lo que tú debes hacer)

### Paso 2.1: Obtener tu API Key de OpenAI

El "cerebro" de los agentes funciona gracias a OpenAI (los creadores de ChatGPT). Para que el código pueda comunicarse con este cerebro, necesitas una "llave" especial llamada API Key.

1.  **Crear una cuenta:** Ve a la plataforma de desarrolladores de OpenAI (platform.openai.com) y regístrate o inicia sesión.
2.  **Configurar facturación:** La API no es gratuita (aunque es muy económica). Ve a **Settings > Billing > Payment methods** y añade una tarjeta de crédito. Luego, ve a **Add to balance** para recargar un saldo inicial (por ejemplo, $5 o $10 dólares) [4].
3.  **Generar la llave:** Ve a la sección **API Keys** en el menú lateral.
4.  **Crear nueva llave:** Haz clic en "Create new secret key", ponle un nombre (ej. "Agentes Contenido") y cópiala inmediatamente. **Importante:** Guárdala en un lugar seguro, ya que no podrás volver a verla completa.

### Paso 2.2: Configurar el entorno local (Tu computadora)

Si deseas ejecutar el código en tu propia computadora en lugar de la nube, necesitas instalar dos programas fundamentales.

1.  **Instalar Python:** Es el lenguaje en el que están escritos los agentes.
    *   Ve a python.org/downloads y descarga la última versión para tu sistema operativo (Windows o Mac).
    *   **Crucial en Windows:** Durante la instalación, asegúrate de marcar la casilla que dice "Add Python to PATH" antes de hacer clic en "Install Now" [5].
2.  **Instalar FFmpeg:** Es el motor que el Productor Multimedia utiliza para cortar los videos y pegar los subtítulos.
    *   **Windows:** Descarga el archivo desde la página oficial de FFmpeg, extráelo en una carpeta (ej. `C:\ffmpeg`) y añade la ruta de la carpeta `bin` a las variables de entorno de tu sistema (PATH) [6].
    *   **Mac:** La forma más fácil es abrir la Terminal y usar Homebrew escribiendo: `brew install ffmpeg`.

### Paso 2.3: Configurar el archivo `.env`

El código necesita saber tu API Key y dónde encontrar los archivos.

1.  En la carpeta del proyecto (`content-agent-beta`), busca el archivo llamado `.env.example`.
2.  Cópialo y renombra la copia a simplemente `.env` (sin la palabra example).
3.  Abre el archivo `.env` con un bloc de notas y reemplaza `sk-tu-api-key-aqui` por la API Key real que obtuviste en el Paso 2.1.

### Paso 2.4: Plataforma de Automatización (n8n o Make.com)

Para que el proceso sea 100% automático cuando un cliente sube un video, necesitas una plataforma que conecte todo. El documento de arquitectura recomienda n8n o Make.com.

1.  **Crear cuenta:** Regístrate en Make.com (más fácil para principiantes) o n8n.cloud.
2.  **Crear un Webhook:** En Make, crea un nuevo "Escenario" y añade un módulo de "Webhook" (Custom Webhook). Esto generará una URL única [7].
3.  **Conectar el Formulario:** Ve a tu cuenta de Tally o Typeform, busca la sección de integraciones/webhooks y pega la URL que te dio Make. Ahora, cada vez que alguien llene el formulario, Make recibirá un aviso.
4.  **Conectar Google Drive:** Añade un módulo de Google Drive en Make para descargar el video que el cliente subió.
5.  **Conectar OpenAI:** Añade módulos de OpenAI en Make para enviar el audio a transcribir (Whisper) y luego enviar el texto a los agentes (GPT-4o-mini).

---

## 3. Ejecución del Sistema (Lo que hace el código)

Una vez que has completado los pasos manuales, el sistema está listo para funcionar. Si lo ejecutas localmente (abriendo la terminal en la carpeta del proyecto y escribiendo `python main.py`), esto es lo que sucede de forma automática:

1.  **Lectura de archivos:** El script lee el video de entrada, la transcripción y el manual de marca desde la carpeta `examples/`.
2.  **Agente 1 (Orquestador):** Se conecta a OpenAI, analiza la transcripción y decide cuáles son los 2 mejores momentos del video para hacer clips virales. Guarda esta decisión en `output/clips_extraidos.json`.
3.  **Agente 2 (Narrativa):** Toma esos clips, lee tu manual de marca, y le pide a OpenAI que escriba los guiones, los textos para redes sociales (copy) y genere los tiempos exactos para los subtítulos. Guarda esto en `output/contenido_final.json`.
4.  **Agente 3 (Productor):** Toma los tiempos de los subtítulos, crea un archivo `.srt` y prepara el comando de FFmpeg para cortar el video original y pegarle los subtítulos con estilo (fuente Montserrat, color blanco, borde negro).

*Nota sobre la versión Beta:* En el código actual, el comando de FFmpeg está preparado pero "comentado" (desactivado por seguridad). Para que realmente corte el video, se debe quitar el símbolo `#` en la línea `subprocess.run(...)` dentro del archivo `multimedia_producer.py`.

---

## Referencias

[1] OpenAI. "Developer quickstart". https://developers.openai.com/api/docs/quickstart/
[2] n8n. "Tutorial: Build an AI workflow in n8n". https://docs.n8n.io/advanced-ai/intro-tutorial/
[3] Tally. "Free Online Form Integrations". https://tally.so/help/integrations
[4] OpenAI Help Center. "How can I set up prepaid billing?". https://help.openai.com/en/articles/8264644-how-can-i-set-up-prepaid-billing
[5] Microsoft Learn. "Python en Windows para principiantes". https://learn.microsoft.com/es-es/windows/dev-environment/python
[6] Transloadit. "How to install FFmpeg on Windows: a complete guide". https://transloadit.com/devtips/how-to-install-ffmpeg-on-windows-a-complete-guide/
[7] Make. "Webhooks Integration". https://www.make.com/en/integrations/gateway
