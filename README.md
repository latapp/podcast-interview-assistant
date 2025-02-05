# Podcast Interview Assistant

Una herramienta de IA para transcribir y analizar entrevistas de podcast, generando preguntas relevantes automáticamente.

## 🚀 Características

- Transcripción automática de audio/video usando Whisper
- Procesamiento de archivos MP3 y MP4
- Generación de preguntas relevantes usando LLM
- Soporte para GPU (CUDA)
- Manejo eficiente de archivos largos mediante fragmentación

## 📋 Requisitos Previos

- Python 3.8+
- CUDA (para aceleración GPU) 
`tambien puede ser cpu, pero es mas lento`
- FFmpeg

## 🔧 Instalación

1. Clonar el repositorio:
```bash
cd podcast_interview_assistant
```

2. Instalar dependencias para 
- #### Linux
    - correr en local:
    ```bash
    pip install -r requirements.txt
    ```
    - correr en la nube usando openai:
    ```bash
    pip install -r requirements_openai.txt
    ```
- #### Windows
    - correr en la nube usando openai:
    ```powershell
    "./install.ps1"
    ```
3. Configurar variables de entorno creando un archivo `.env` en el directorio raíz del proyecto con las siguientes variables:

```bash
API_KEY=<API_KEY>
MODEL_BASE_URL=[base_url] #solo en caso de usar servidores alternativos o locales, como ollama o deepseek
```

## 💻 Uso

1. Coloca tu archivo de audio/video en el directorio del proyecto
2. Ejecuta el script principal:
    - #### Linux
    
    ```bash
    python main.py <file path>
    ```
    - #### Windows
    ```powershell
    "./run.ps1"
    ```

3. El programa generará un archivo `output.json` con las preguntas generadas

## ⚙️ Configuración

Puedes modificar los siguientes parámetros en `config/config.py`:
- `WHISPER_MODEL`: Modelo de Whisper a utilizar
- `FRAGMENT_DURATION`: Duración de los fragmentos de audio
- `BASE_PROMPT`: Prompt base para el LLM


