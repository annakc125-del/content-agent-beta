# Guía de Configuración de Agentes IA (Adaptada para Celular)

**Autor:** Manus AI
**Fecha:** Abril 2026

Esta guía responde a tus dudas sobre la seguridad de la API Key y explica cómo continuar la configuración de tu ecosistema de agentes IA trabajando exclusivamente desde tu dispositivo móvil.

---

## 1. Aclaración sobre `.env`, `.gitignore` y la API Key

Entiendo perfectamente tu confusión. Aquí te explico cómo funciona la seguridad en GitHub de forma sencilla:

*   **¿Qué es el archivo `.env`?** Es un archivo de texto simple donde guardas contraseñas y claves secretas (como tu API Key de OpenAI).
*   **¿Por qué no debe subirse a GitHub?** Porque si tu repositorio es público (o si alguien más tiene acceso), podrían ver tu clave y usar tu saldo de OpenAI.
*   **¿Qué es el archivo `.gitignore`?** Es una lista de "reglas" que le dice a GitHub: *"Ignora estos archivos, nunca los subas a internet"*.

**Lo que acabo de hacer por ti:**
1.  Me di cuenta de que tu repositorio **no tenía** un archivo `.gitignore`.
2.  Acabo de crear el `.gitignore` y lo subí a tu repositorio. En él, puse la regla estricta de que el archivo `.env` **nunca** debe subirse.
3.  También creé una plantilla del archivo `.env` en mi entorno de trabajo (sandbox).

**¿Cómo funciona si solo queda en mi entorno de trabajo?**
Como el `.env` está protegido por el `.gitignore`, si yo lo creo aquí, se queda aquí. Cuando tú descargues (clones) el código en otra computadora o servidor en el futuro, el archivo `.env` no existirá allí. Tendrás que crearlo manualmente en esa nueva computadora y pegar tu clave.

**La solución más segura (y la que aplicaremos):**
He dejado un archivo llamado `.env.example` en tu repositorio de GitHub. Ese archivo **sí** se sube a internet porque no tiene tu clave real, solo tiene texto de ejemplo. Cuando estés listo para ejecutar el código (ya sea en una computadora o en un servidor en la nube), copiarás ese archivo, lo renombrarás a `.env` y pegarás tu clave real.

---

## 2. Trabajando desde el Celular: ¿Es posible?

**Sí, es posible configurar casi todo desde el celular**, pero con algunas limitaciones importantes que debes conocer.

### Lo que SÍ puedes hacer desde el celular (Configuración de Plataformas)

1.  **OpenAI (API Key):** Ya lo hiciste. ¡Perfecto!
2.  **Tally (Formularios):** Puedes crear y editar formularios desde el navegador de tu celular (Chrome/Safari) entrando a tally.so. Tienen una interfaz que se adapta decentemente a pantallas pequeñas [1].
3.  **Google Drive:** Puedes crear carpetas y organizar archivos usando la aplicación oficial de Google Drive para iOS o Android.
4.  **Make.com (Automatización):** Puedes entrar a Make.com desde el navegador de tu celular para crear la cuenta y conectar las aplicaciones. **Advertencia:** La interfaz de Make.com (donde arrastras y conectas "bolitas" o nodos) es muy difícil de manejar en una pantalla táctil pequeña [2]. Te recomiendo usar una tablet o tener mucha paciencia si lo haces desde el teléfono.

### Lo que NO puedes hacer fácilmente desde el celular (Ejecutar el Código)

El código de Python (los agentes) necesita un lugar donde "correr" o ejecutarse.

*   **No puedes instalar Python ni FFmpeg directamente en tu celular** de la misma forma que en una computadora.
*   **La solución en la nube:** Como estás en celular, la mejor alternativa es usar un servicio en la nube gratuito como **Google Colab** o **PythonAnywhere** [3]. Estos servicios te prestan una "computadora virtual" a la que accedes desde el navegador de tu celular. Allí puedes descargar tu código de GitHub, crear el archivo `.env`, pegar tu API Key y ejecutar los agentes.

---

## 3. Próximos Pasos (Desde tu Celular)

Ya que tienes tu API Key, estos son los pasos exactos que debes seguir desde tu dispositivo móvil:

### Paso 1: Crear el Formulario en Tally
1.  Abre el navegador de tu celular y ve a tally.so.
2.  Crea un formulario nuevo pidiendo: Nombre del cliente, Enlace al video original (YouTube o Drive), y Enlace al manual de marca.
3.  Guarda el formulario. Aún no configures el webhook, lo haremos en el siguiente paso.

### Paso 2: Preparar Google Drive
1.  Abre la app de Google Drive en tu celular.
2.  Crea una carpeta principal llamada `Agentes_Contenido`.
3.  Dentro, crea dos subcarpetas: `Entradas` (para los videos de los clientes) y `Salidas` (para los videos finales).

### Paso 3: Configurar Make.com (El paso más difícil en celular)
1.  Ve a Make.com en tu navegador móvil y crea una cuenta.
2.  Crea un nuevo "Scenario" (Escenario).
3.  Añade el primer módulo: busca "Webhooks" y selecciona "Custom webhook". Esto te dará una URL larga. Cópiala.
4.  Vuelve a Tally, ve a la configuración de tu formulario, busca "Integrations" > "Webhooks" y pega la URL de Make.com.
5.  Vuelve a Make.com y añade los siguientes módulos conectándolos al webhook:
    *   **Google Drive:** Para descargar el video.
    *   **OpenAI (Whisper):** Para transcribir el audio.
    *   **OpenAI (GPT-4o-mini):** Para que los agentes analicen el texto.

### Paso 4: Ejecutar el código (Alternativa en la nube)
Cuando tengas todo conectado y quieras probar el código de Python:
1.  Abre **Google Colab** (colab.research.google.com) en el navegador de tu celular.
2.  Crea un nuevo "Notebook".
3.  Allí podrás escribir comandos para descargar tu código de GitHub (`!git clone https://github.com/annakc125-del/content-agent-beta.git`), crear el archivo `.env` con tu API Key, y ejecutar el script principal (`!python main.py`).

---

## Referencias

[1] Tally. "Creating your first Tally form". https://tally.so/help/create-a-form
[2] Make. "Make: AI Workflow Automation Software & Tools". https://www.make.com/en
[3] Reddit Community. "¿Cuáles son algunas maneras gratuitas de ejecutar Python?". https://www.reddit.com/r/Python/comments/12xse2k/what_are_some_free_ways_to_run_python_24x7/
