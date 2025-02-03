####  GENERAL SETTINGS   ####

BASE_PROMPT = "Se te enviara la transcripcion de un podcast, tu tarea es analizar el podcast y generar preguntas para una entrevista, , deben ser preguntas enfocadas hacia el entrevistado, con cierta picardia y humor, pero sin faltar el respeto. El podcast es chileno y todo debe estar relacionado con el entrevistado"


####   TRANSCRIPTOR SETTINGS   ####

FRAGMENT_DURATION = 1000
WHISPER_MODEL = "large"
DEVICE = "cuda" # "cuda" or "cpu"


####   LLM SETTINGS   ####

LLM_MODEL = "phi4"
LLM_MODEL_API_KEY = "ollama"
LLM_MODEL_BASE_URL = "http://localhost:11434/v1"