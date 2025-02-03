from LLM import LLM
from transcription import Transcriptor
from sys import argv
from utils import TimeChecker



if len(argv) <= 1:
    print("INGRESE EL ARCHIVO DE AUDIO A TRANSCRIBIR\n\n")
    print("Usage: python main.py <audio_file>")
    
description_podcast = input("Ingrese una breve descripción del podcast: ")


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
        # save in file
        with open("output.json", "w") as f:
            f.write(response)
    
    except Exception as e:
        print(e)
    finally:
        print("Cleaning up")
        time_checker.stop()
        time_checker._print()

if __name__ == "__main__":
    main()