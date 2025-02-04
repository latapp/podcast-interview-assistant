from dotenv import load_dotenv
import os



####  GENERAL SETTINGS   ####

BASE_PROMPT = "Se te enviara la transcripcion de un podcast, tu tarea es analizar el podcast y generar preguntas para una entrevista, , deben ser preguntas enfocadas hacia el entrevistado, con cierta picardia y humor, pero sin faltar el respeto. El podcast es chileno y todo debe estar relacionado con el entrevistado"
MODEL_API_KEY = "ollama"
MODEL_BASE_URL = None #if None, use the default url from openai


####   TRANSCRIPTOR SETTINGS   ####

FRAGMENT_DURATION = 180
LOCAL_MODE = False

# region the local mode disable this settings
WHISPER_MODEL = "large"
DEVICE = "cuda" # "cuda" or "cpu"
# endregion

####   LLM SETTINGS   ####

LLM_MODEL = "gpt-4o"


####  ENVIRONMENT VARIABLES   ####
ok = load_dotenv()
if ok:
    print(".env encontrado, cargando variables de entorno")
    
    if os.getenv("API_KEY"):
        MODEL_API_KEY = os.getenv("API_KEY")
    if os.getenv("MODEL_BASE_URL"):
        MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")
