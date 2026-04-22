# Guía de Configuración y Programación de Agentes IA desde Dispositivo Móvil

**Autor:** Manus AI
**Fecha:** Abril 2026

Esta guía está diseñada para usuarios que desean configurar y, en la medida de lo posible, programar sus agentes de IA directamente desde un dispositivo móvil (smartphone o tablet). Abordaremos los ajustes necesarios en el dispositivo, las herramientas móviles recomendadas y cómo adaptar cada plataforma del ecosistema para un flujo de trabajo móvil.

---

## 1. Ajustes de Desarrollador en tu Dispositivo Móvil

Para algunas tareas avanzadas, especialmente si planeas conectar tu dispositivo a una computadora o usar ciertas aplicaciones de terminal, puede ser útil activar las opciones de desarrollador. Sin embargo, para la mayoría de los pasos de esta guía (uso de plataformas web y Google Colab), **no son estrictamente necesarias**.

### 1.1. Android: Activación de Opciones de Desarrollador

Las Opciones de Desarrollador en Android permiten configurar comportamientos del sistema para depuración y perfilado. Para activarlas [1]:

1.  Ve a **Ajustes** (Settings) en tu dispositivo.
2.  Desplázate hasta el final y selecciona **Acerca del teléfono** (About phone).
3.  Busca la opción **Número de compilación** (Build number). La ubicación exacta puede variar según el fabricante (ver Tabla 1).
4.  Toca el **Número de compilación** **siete veces** consecutivas. Verás un mensaje que dice: "¡Ya eres desarrollador!" (You are now a developer!).
5.  Regresa a la pantalla anterior de Ajustes. Ahora verás **Opciones de desarrollador** (Developer options) en la parte inferior del menú.

**Tabla 1. Ubicación del 'Número de compilación' en diferentes dispositivos Android**

| Dispositivo         | Ruta en Ajustes                                    |
| :------------------ | :------------------------------------------------- |
| Google Pixel        | Ajustes > Acerca del teléfono > Número de compilación |
| Samsung Galaxy S8+  | Ajustes > Acerca del teléfono > Información de software > Número de compilación |
| LG G6+              | Ajustes > Acerca del teléfono > Información de software > Número de compilación |
| OnePlus 5T+         | Ajustes > Acerca del teléfono > Número de compilación |

**Opciones útiles en el Modo Desarrollador (si las necesitas):**

*   **Depuración USB (USB debugging):** Permite que tu dispositivo se comunique con una computadora a través de ADB (Android Debug Bridge) para depurar aplicaciones. Útil si en algún momento conectas tu teléfono a una PC para desarrollo [1].
*   **Depuración inalámbrica (Wireless debugging):** Similar a la Depuración USB, pero permite la conexión a través de Wi-Fi. Disponible en Android 11 (API nivel 30) y superior [1].

### 1.2. iOS (iPhone/iPad): Activación del Modo Desarrollador

En iOS, el Modo Desarrollador es necesario principalmente para instalar y probar aplicaciones que no provienen de la App Store (sideloading) o para depurar aplicaciones con Xcode. Para la mayoría de los casos de esta guía (uso de terminales o entornos en la nube), **puede que no sea necesario activarlo** [2].

1.  Abre la aplicación **Ajustes** (Settings).
2.  Navega hasta **Privacidad y Seguridad** (Privacy & Security).
3.  Desplázate hacia abajo y busca **Modo Desarrollador** (Developer Mode).
4.  Activa el interruptor. Es posible que se te pida reiniciar el dispositivo.

**Nota importante:** En algunas versiones de iOS, la opción "Modo Desarrollador" solo aparece después de haber conectado el iPhone/iPad a una Mac con Xcode instalado al menos una vez [2].

---

## 2. Herramientas Móviles Esenciales para Programar

Dado que trabajarás desde el celular, necesitarás aplicaciones que te permitan interactuar con el código y el sistema.

### 2.1. Gestión de Código: GitHub Mobile App

La aplicación oficial de GitHub para iOS y Android te permite ver tus repositorios, revisar código, gestionar issues y pull requests. Aunque no es un editor de código completo, es excelente para monitorear tu proyecto y hacer pequeñas ediciones [3].

*   **Descarga:** Busca "GitHub" en la App Store (iOS) o Google Play Store (Android).

### 2.2. Terminal y Ejecución de Python

Aquí es donde el trabajo "real" de programación se diferencia entre Android e iOS.

#### Para Android: Termux (Recomendado)

**Termux** es un emulador de terminal potente que te brinda un entorno Linux completo en tu Android, sin necesidad de root. Puedes instalar Python, Git y muchas otras herramientas de línea de comandos [4].

*   **Descarga:** **NO** lo descargues de Google Play Store, ya que está desactualizado. Descárgalo desde **F-Droid** (f-droid.org) [5].
    1.  Visita `https://f-droid.org` en tu navegador móvil y descarga el APK de F-Droid.
    2.  Instala F-Droid (puede que necesites habilitar "Instalar aplicaciones de fuentes desconocidas" en los ajustes de seguridad de tu Android).
    3.  Abre F-Droid, busca "Termux" e instálalo.
*   **Configuración inicial en Termux:**
    ```bash
pkg update && pkg upgrade
pkg install git python curl wget nano openssh
termux-setup-storage
    ```
    *   `pkg update && pkg upgrade`: Actualiza los paquetes del sistema.
    *   `pkg install ...`: Instala Git (para clonar tu repositorio), Python (para ejecutar tus scripts), curl y wget (para descargar archivos), nano (un editor de texto simple) y openssh (para conexiones remotas si las necesitas).
    *   `termux-setup-storage`: Solicita permisos para que Termux acceda al almacenamiento interno de tu teléfono. **Acepta el permiso cuando te lo pida.**

#### Para iOS: a-Shell (Recomendado) o iSH

**a-Shell** es un terminal Unix local para iOS que incluye Python, Git y otras herramientas. Permite ejecutar scripts directamente en tu iPhone o iPad [6].

*   **Descarga:** Busca "a-Shell" en la App Store.
*   **Configuración inicial en a-Shell:**
    *   `pip install --upgrade pip`
    *   `pip install openai python-dotenv` (para las librerías de tus agentes)
    *   `git clone [URL_DE_TU_REPOSITORIO]` (para descargar tu código)

**iSH Shell** es otra opción que emula un entorno Linux completo (Alpine Linux) en iOS. También permite instalar Python y Git [7].

*   **Descarga:** Busca "iSH Shell" en la App Store.
*   **Configuración inicial en iSH:**
    ```bash
apk update && apk upgrade
apk add python3 py3-pip git
    ```
    *   `apk update && apk upgrade`: Actualiza los paquetes.
    *   `apk add python3 py3-pip git`: Instala Python 3, pip y Git.

**Alternativa (de pago): Pythonista**

**Pythonista** es un IDE de Python completo para iOS, con editor de código, consola interactiva y soporte para muchas librerías. Es una excelente opción si buscas una experiencia de desarrollo más integrada, pero es de pago [8].

---

## 3. Configuración del Ecosistema de Agentes IA (Paso a Paso Móvil)

Ahora, vamos a configurar las plataformas necesarias, adaptando los pasos para tu flujo de trabajo móvil.

### Paso 0: Preparación del Repositorio (Ya hecho por Manus)

Ya me encargué de:
*   Crear el archivo `.gitignore` en tu repositorio de GitHub para asegurar que tu archivo `.env` (con tu API Key) nunca se suba accidentalmente.
*   Dejar el archivo `.env.example` en tu repositorio. Este es un ejemplo público de cómo debe lucir tu `.env`.

### Paso 1: Obtener tu API Key de OpenAI

(Ya lo tienes, ¡excelente!)

1.  Si aún no lo has hecho, ve a `platform.openai.com` en el navegador de tu celular.
2.  Regístrate, añade un método de pago y carga algo de saldo (por ejemplo, $5-10 USD para empezar).
3.  Genera tu API Key secreta (empieza con `sk-...`). **Guárdala en un lugar seguro, como un gestor de contraseñas.**

### Paso 2: Configurar el archivo `.env` (en tu entorno de ejecución móvil)

Este es un paso CRÍTICO. El archivo `.env` contiene tu clave secreta y solo debe existir en el lugar donde ejecutes el código.

#### Opción A: Usando Google Colab (Recomendado para ambos sistemas)

Google Colab te permite ejecutar código Python en la nube desde tu navegador móvil. Es la opción más sencilla para empezar.

1.  Abre `colab.research.google.com` en el navegador de tu celular.
2.  Crea un nuevo "Notebook".
3.  En una celda de código, clona tu repositorio de GitHub:
    ```python
!git clone https://github.com/annakc125-del/content-agent-beta.git
%cd content-agent-beta
    ```
4.  En otra celda, crea el archivo `.env` y pega tu API Key. **Asegúrate de reemplazar `PEGA-TU-API-KEY-AQUI` con tu clave real.**
    ```python
%%writefile .env
# ============================================================
# ARCHIVO DE CONFIGURACIÓN - AGENTES IA (Beta)
# ============================================================
# INSTRUCCIONES: Reemplaza PEGA-TU-API-KEY-AQUI por tu clave
# real de OpenAI (empieza con sk-...)
# ============================================================

# Configuración de OpenAI API (OBLIGATORIO)
OPENAI_API_KEY=PEGA-TU-API-KEY-AQUI

# Configuración de rutas de entrada/salida
INPUT_VIDEO=examples/video_fuente.mp4
INPUT_TRANSCRIPTION=examples/transcripcion.txt
BRAND_GUIDELINES=examples/manual_marca.txt
OUTPUT_DIR=output

# Configuración de notificaciones (Opcional - para el flujo completo)
EMAIL_TO=cliente@ejemplo.com
EMAIL_FROM=noreply@tu-dominio.com
SMTP_SERVER=smtp.ejemplo.com
SMTP_PORT=587
SMTP_USER=tu-usuario
SMTP_PASSWORD=tu-password
    ```
5.  Luego, puedes instalar las dependencias y ejecutar tu script:
    ```python
!pip install -r requirements.txt # Si tienes un archivo requirements.txt
!python main.py
    ```

#### Opción B: Usando Termux (Solo Android)

1.  Abre Termux.
2.  Clona tu repositorio:
    ```bash
git clone https://github.com/annakc125-del/content-agent-beta.git
cd content-agent-beta
    ```
3.  Copia el archivo de ejemplo y edítalo con `nano` para pegar tu API Key:
    ```bash
cp .env.example .env
nano .env
    ```
    *   Dentro de `nano`, busca `OPENAI_API_KEY=PEGA-TU-API-KEY-AQUI` y reemplaza `PEGA-TU-API-KEY-AQUI` con tu clave real.
    *   Guarda el archivo (Ctrl+O, luego Enter) y sal de nano (Ctrl+X).
4.  Instala las dependencias (si tienes `requirements.txt`):
    ```bash
pip install -r requirements.txt
    ```
5.  Ejecuta tu script:
    ```bash
python main.py
    ```

#### Opción C: Usando a-Shell o iSH (Solo iOS)

1.  Abre a-Shell o iSH.
2.  Clona tu repositorio:
    ```bash
git clone https://github.com/annakc125-del/content-agent-beta.git
cd content-agent-beta
    ```
3.  Copia el archivo de ejemplo y edítalo. a-Shell tiene un editor `edit` o puedes usar `nano` si lo instalaste en iSH:
    *   **a-Shell:**
        ```bash
cp .env.example .env
edit .env
        ```
        Pega tu API Key y guarda.
    *   **iSH (con nano):**
        ```bash
cp .env.example .env
nano .env
        ```
        Pega tu API Key, guarda (Ctrl+O, Enter) y sal (Ctrl+X).
4.  Instala las dependencias (si tienes `requirements.txt`):
    ```bash
pip install -r requirements.txt
    ```
5.  Ejecuta tu script:
    ```bash
python main.py
    ```

### Paso 3: Crear el Formulario en Tally

1.  Abre el navegador de tu celular y ve a `tally.so`.
2.  Crea una cuenta o inicia sesión.
3.  Crea un nuevo formulario (`+ New form`).
4.  Añade los campos necesarios para que tus clientes suban información. Sugerencias:
    *   **Nombre del Cliente** (Short text)
    *   **Correo Electrónico del Cliente** (Email)
    *   **Enlace al Video Original** (URL) - Aquí el cliente pegará un enlace a su video (ej. YouTube, Google Drive, Dropbox).
    *   **Enlace al Manual de Marca/Guías** (URL, opcional) - Para que el cliente comparta sus preferencias de marca.
5.  Personaliza el diseño a tu gusto.
6.  Guarda el formulario. **Todavía no configures el webhook aquí.**

### Paso 4: Preparar Google Drive

Google Drive será tu almacenamiento para los videos de entrada y los resultados finales.

1.  Abre la aplicación **Google Drive** en tu celular (o accede vía navegador).
2.  Crea una carpeta principal para tu proyecto, por ejemplo, `Agentes_IA_Contenido`.
3.  Dentro de esta carpeta, crea dos subcarpetas:
    *   `Entradas_Videos`: Aquí se guardarán los videos que tus clientes suban (o enlaces a ellos).
    *   `Salidas_Procesadas`: Aquí se almacenarán los videos finales generados por los agentes.
4.  Asegúrate de que estas carpetas tengan los permisos adecuados si necesitas compartirlas con Make.com o con tus clientes.

### Paso 5: Configurar Make.com o n8n (Flujo de Automatización)

Esta es la parte más compleja desde un celular debido a la interfaz visual de arrastrar y soltar. Si tienes acceso a una tablet o computadora, te lo recomiendo encarecidamente para este paso. Si no, ten paciencia.

1.  Abre el navegador de tu celular y ve a `make.com` o `n8n.io`.
2.  Crea una cuenta o inicia sesión.
3.  **Crea un nuevo "Scenario" (Make.com) o "Workflow" (n8n).**
4.  **Primer Módulo: Webhook (Disparador)**
    *   Busca y añade un módulo de **Webhook** (Custom Webhook en Make.com).
    *   Copia la URL que te proporciona el webhook. Esta URL es el "punto de entrada" para tu automatización.
5.  **Conectar Tally con el Webhook:**
    *   Vuelve a `tally.so` en tu navegador.
    *   Edita tu formulario (creado en el Paso 3).
    *   Ve a **Integrations** (Integraciones) y busca **Webhooks**.
    *   Pega la URL del webhook de Make.com/n8n que copiaste en el paso anterior.
    *   Envía un envío de prueba desde Tally para que Make.com/n8n detecte la estructura de los datos.
6.  **Siguientes Módulos (Ejemplo de flujo):**
    *   **Google Drive (Descargar archivo):** Conecta este módulo para que, cuando el webhook reciba un enlace de video, lo descargue a tu carpeta `Entradas_Videos` en Google Drive.
    *   **OpenAI (Whisper - Transcripción):** Conecta este módulo para transcribir el audio del video descargado. Necesitarás tu API Key de OpenAI aquí.
    *   **Módulo de Código/HTTP (Ejecutar Agentes IA):** Aquí es donde la cosa se pone más avanzada. Si estás usando Google Colab, Termux o a-Shell para ejecutar tus agentes, necesitarás un módulo que pueda:
        *   **Enviar la transcripción y otros datos** (manual de marca, etc.) a tu entorno de ejecución (Colab, Termux, etc.). Esto podría ser a través de una API que expongas desde Colab/Termux (más complejo) o simplemente que tus agentes "lean" directamente de Google Drive.
        *   **Disparar la ejecución de tus agentes.**
    *   **Google Drive (Subir archivo):** Una vez que tus agentes hayan procesado el video y generado el contenido, este módulo subirá el resultado a tu carpeta `Salidas_Procesadas`.
    *   **Email (Notificación):** Para enviar un correo al cliente con el enlace al video final.

**Advertencia:** La construcción de flujos complejos en Make.com o n8n desde un celular puede ser frustrante. La interfaz de arrastrar y soltar no está optimizada para pantallas pequeñas. Considera usar una tablet o una computadora para esta parte si te resulta muy difícil.

### Paso 6: Ejecutar el Código de los Agentes (Alternativas Móviles)

Aquí es donde tus scripts de Python con los agentes de IA cobrarán vida. Como mencionamos, no puedes ejecutarlos directamente en el sistema operativo de tu celular, pero tienes excelentes alternativas.

#### Opción A: Google Colab (Recomendado para ambos sistemas)

Es la forma más sencilla de ejecutar tu código Python en un entorno Linux en la nube, accesible desde el navegador de tu celular.

1.  Abre tu Notebook de Colab (donde ya clonaste el repo e hiciste el `.env`).
2.  Asegúrate de que todas las dependencias estén instaladas (`!pip install -r requirements.txt`).
3.  Ejecuta tu script principal (ej. `!python main.py`).
4.  **Integración con Make.com/n8n:** Para que Make.com/n8n pueda "hablar" con Colab y disparar la ejecución, necesitarías exponer una API desde Colab (usando `ngrok` o `flask-ngrok`), lo cual añade complejidad. Una alternativa más simple es que tus agentes en Colab monitoreen una carpeta específica en Google Drive para nuevos archivos de entrada, y Make.com/n8n simplemente coloque los archivos allí.

#### Opción B: Termux (Solo Android)

Si prefieres un control más directo y un entorno Linux local en tu Android:

1.  Abre Termux y navega a la carpeta de tu repositorio (`cd content-agent-beta`).
2.  Asegúrate de que tu `.env` esté configurado con tu API Key.
3.  Instala FFmpeg (necesario para el agente `multimedia_producer.py`):
    ```bash
pkg install ffmpeg
    ```
4.  Instala las librerías de Python (`pip install -r requirements.txt`).
5.  Ejecuta tu script principal:
    ```bash
python main.py
    ```
6.  **Integración con Make.com/n8n:** Similar a Colab, la integración directa es compleja. Podrías usar `termux-api` para notificaciones o incluso un pequeño servidor web en Python (`Flask`, `FastAPI`) expuesto a través de `ngrok` para recibir disparadores de Make.com/n8n, pero esto requiere conocimientos avanzados de redes y seguridad.

#### Opción C: a-Shell o iSH (Solo iOS)

Si estás en iOS y quieres ejecutar localmente:

1.  Abre a-Shell o iSH y navega a la carpeta de tu repositorio.
2.  Asegúrate de que tu `.env` esté configurado con tu API Key.
3.  Instala FFmpeg (si está disponible en tu terminal, en a-Shell puede que ya esté o se instale con `pkg install ffmpeg` o similar, en iSH con `apk add ffmpeg`).
4.  Instala las librerías de Python (`pip install -r requirements.txt`).
5.  Ejecuta tu script principal:
    ```bash
python main.py
    ```
6.  **Integración con Make.com/n8n:** Muy similar a Termux, la integración directa es un desafío. La opción más viable es usar Google Drive como punto de intercambio de archivos y que tus agentes monitoreen esa carpeta.

---

## 4. Consideraciones Adicionales

*   **FFmpeg:** Tu agente `multimedia_producer.py` requiere FFmpeg. Asegúrate de instalarlo en tu entorno de ejecución (ya sea Colab, Termux o iSH/a-Shell). En Colab, suele estar preinstalado o se instala fácilmente con `!apt-get install ffmpeg`. En Termux/iSH, usa `pkg install ffmpeg` o `apk add ffmpeg`.
*   **Persistencia:** Si ejecutas tus agentes en Termux o iSH/a-Shell, ten en cuenta que las sesiones pueden cerrarse si la aplicación se va a segundo plano o el dispositivo se reinicia. Para procesos largos, considera usar `tmux` (en Termux) o ejecutar scripts en segundo plano si la terminal lo permite.
*   **Rendimiento:** La ejecución de modelos de IA y procesamiento de video puede consumir muchos recursos. Un celular tendrá limitaciones de rendimiento y batería en comparación con una computadora o un servidor en la nube.

---

## Referencias

[1] Android Developers. "Configure on-device developer options". `https://developer.android.com/studio/debug/dev-options`
[2] Apple Developer. "Enabling Developer Mode on a device". `https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device`
[3] GitHub. "GitHub Mobile". `https://github.com/mobile`
[4] Termux. "Termux Wiki". `https://wiki.termux.com/wiki/Main_Page`
[5] Termux Genius. "The Complete Guide to Termux Setup Commands for Android (2026)". `https://www.termuxgenius.com/2025/10/termux-setup-command-android-2025.html`
[6] a-Shell. "A terminal for iOS, with multiple windows". `https://github.com/holzschu/a-shell`
[7] iSH. "iSH Shell". `https://ish.app/`
[8] Pythonista. "Pythonista for iOS". `http://omz-software.com/pythonista/`
