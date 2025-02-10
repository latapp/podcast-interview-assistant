from dotenv import load_dotenv
import os



####  GENERAL SETTINGS   ####

BASE_PROMPT = "Se te enviara la transcripcion de un podcast, tu tarea es generar 3 preguntas para una entrevista, ademas de esto dar tu opinion propia, si crees que es interesante o no, si de forma simulada te provoca alguna emocion esto sin resumir el podcast en tu opinion, deben ser preguntas enfocadas hacia el entrevistado, con cierta picardia y humor, pero sin faltar el respeto, que provoquen cierto desafio para el entrevistador. El podcast es chileno y todo debe estar relacionado con el entrevistado, tocando temas como el arte, la ciencia, la tecnologia o la politica, el publico objetivo de este mismo son personas de 25 a 55 años, con un nivel de educacion universitaria, que buscan informacion y entretenimiento de calidad. "
MODEL_API_KEY = "ollama"
MODEL_BASE_URL = None #if None, use the default url from openai


####   TRANSCRIPTOR SETTINGS   ####

FRAGMENT_DURATION = 180
LOCAL_MODE = False

# region the non local mode disable this settings
WHISPER_MODEL = "turbo"
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
