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

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de configuracion en el archivo config:

```python
LLM_MODEL_API_KEY=tu_api_key
LLM_MODEL_BASE_URL=url_del_modelo
```

## 💻 Uso

1. Coloca tu archivo de audio/video en el directorio del proyecto
2. Ejecuta el script principal:
```bash
python main.py
```

3. El programa generará un archivo `output.json` con las preguntas generadas

## ⚙️ Configuración

Puedes modificar los siguientes parámetros en `config/config.py`:
- `WHISPER_MODEL`: Modelo de Whisper a utilizar
- `FRAGMENT_DURATION`: Duración de los fragmentos de audio
- `BASE_PROMPT`: Prompt base para el LLM

