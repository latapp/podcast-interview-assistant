import json
import os 
from LLM import LLM
from transcription import Transcriptor
from sys import argv
from utils import TimeChecker


os.makedirs("output", exist_ok=True)
if len(argv) <= 1:
    print("INGRESE EL ARCHIVO DE AUDIO A TRANSCRIBIR\n\n")
    print("Usage: python main.py <audio_file>")
    exit(1)
    
description_podcast = "Desde La Araucanía, Camilo Klein - fundador del Biergarten-, entrevista a diversos exponentes del ámbito cultural, científico, político y empresarial"
filename = argv[1].split("/")[-1].split(".")[0]

def main():
    time_checker = TimeChecker()
    # Comienza a contar el tiempo
    time_checker.start()
    transcriptor = Transcriptor(
        description_podcast
    )
    llm = LLM()
    try:
        # Transcribe the audio
        print("making transcription...")
        transcription = transcriptor.transcribe(argv[1])
        # Generate questions
        print("creating questions...")
        response = llm.generate(transcription)
        json_data = json.loads(response)
        questions = json_data["questions"]
        with open(f"output/preguntas {filename}.txt", "w") as f:

            f.write(f"Podcast: {description_podcast}\n\n")
            f.write(f"Opinion: {json_data['opinion']}\n\n\n")
            #preguntas
            for question in questions:
                f.write(f"- {question}\n\n")
            
    
    except Exception as e:
        print(e)
    finally:
        time_checker.stop()
        transcriptor.cleanup()

if __name__ == "__main__":
    main()