# Ecosistema de Agentes de IA - Microservicio de Creación de Contenido (Beta)

Este repositorio contiene el código fuente y la documentación de la versión Beta (MVP) del Ecosistema de Agentes de Inteligencia Artificial diseñado para automatizar la creación de contenido multimedia (Reels, Shorts, TikToks, Carruseles) a partir de videos largos.

## 🚀 Propuesta de Valor

Transformar contenido existente (podcasts, webinars, videos de YouTube) en micro-contenido optimizado para redes sociales, ahorrando tiempo masivo y manteniendo la autenticidad de la marca mediante la aplicación estricta de manuales de estilo.

## 🏗️ Arquitectura del Sistema (Beta)

El sistema está compuesto por 3 agentes principales:

1.  **Orquestador y Curador (El Director):** Analiza la transcripción del video original y selecciona los mejores fragmentos basándose en heurísticas de retención y potencial viral.
2.  **Creador de Narrativa (El Guionista):** Adapta los fragmentos seleccionados, genera guiones optimizados, subtítulos dinámicos y redacta el copy para las redes sociales, asegurando la coherencia con la identidad de la marca.
3.  **Productor Multimedia (El Editor):** Ejecuta los cortes de video y aplica subtítulos básicos utilizando FFmpeg.

## 📁 Estructura del Proyecto

*   `/agents`: Código fuente en Python de los 3 agentes.
*   `/prompts`: Prompts del sistema utilizados por los agentes (Orquestador y Creador de Narrativa).
*   `/docs`: Documentación detallada, incluyendo el diseño de la arquitectura Beta y ejemplos de entrega.
*   `/examples`: Archivos JSON de ejemplo generados por el sistema (scripts y carruseles).
*   `main.py`: Script principal que orquesta el flujo de trabajo.
*   `.env.example`: Plantilla de variables de entorno.

## ⚙️ Instalación y Uso

### Requisitos Previos

*   Python 3.8+
*   FFmpeg instalado en el sistema (`sudo apt install ffmpeg` en Ubuntu/Debian)
*   Clave de API de OpenAI

### Pasos de Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/annakc125-del/content-agent-beta.git
    cd content-agent-beta
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install openai python-dotenv
    ```

3.  **Configurar variables de entorno:**
    Copia el archivo `.env.example` a `.env` y añade tu clave de API de OpenAI.
    ```bash
    cp .env.example .env
    # Edita .env con tu editor favorito
    ```

4.  **Preparar archivos de entrada:**
    Coloca tu video fuente, transcripción y manual de marca en la carpeta `examples/` (o actualiza las rutas en el archivo `.env`).

5.  **Ejecutar el flujo:**
    ```bash
    python main.py
    ```

Los resultados (archivos JSON y videos procesados) se guardarán en la carpeta `output/`.

## 🗺️ Roadmap

*   **v1.0 (Actual - Beta):** Flujo lineal básico, curaduría por LLM, subtítulos estáticos con FFmpeg.
*   **v2.0:** Análisis de tendencias en tiempo real, subtítulos dinámicos estilo "Hormozi" (animación palabra por palabra), publicación automática en redes sociales.
*   **v3.0:** Generación de carruseles de imágenes con DALL-E 3, transición a framework de orquestación de agentes puro (CrewAI/LangGraph), integración con herramientas de analytics.

## 📄 Documentación Adicional

Consulta la carpeta `/docs` para obtener información más detallada sobre el diseño del ecosistema y ejemplos de entregables.
