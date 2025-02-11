from ast import parse
import json
from LLM.llm import LLM
import os
from transcriptor_srt.transcriptor_processor import TranscriptionProcessor
from utils.time_checker import TimeChecker
import argparse
from colorama import Fore

description_podcast = "Desde La Araucanía, Camilo Klein - fundador del Biergarten-, entrevista a diversos exponentes del ámbito cultural, científico, político y empresarial"

#region parse arguments
parser = argparse.ArgumentParser(description="Generador de preguntas a partir de un archivo de audio")

parser.add_argument("-i","--input", type=str, help="Archivo o ruta de audio a transcribir", default="./input")
parser.add_argument("-m","--model", type=str, help="Modelo de lenguaje a utilizar", default="gpt-4o")
parser.add_argument("-o","--output", type=str, help="Ruta de salida para los archivos generados", default="./output")
parser.add_argument("-wm", "--whisper-model", type=str, help="Modelo para trancripcion(solo disponible en modo local)", default="turbo")
parser.add_argument("--srtinput", type=str, help="Archivo srt para generar las preguntas sin transcribir el audio")
parser.add_argument("--local", action="store_true", help="Modo local para transcripcion")
parser.add_argument("--srt", action="store_true", help="habilitar la generacion del archivo srt")

arguments = parser.parse_args()
print("Starting...")

is_folder = os.path.isdir(arguments.input)

if is_folder:
    files = os.listdir(arguments.input)
else:
    files = [arguments.input]


llm = LLM()


for file in files:
    # get full path
    file = os.path.abspath(file)
    print(f"{Fore.GREEN}Procesando archivo: {file}{Fore.RESET}")
    base_output = arguments.output
    filename = os.path.basename(file).split(".")[0]
    output = os.path.join(base_output, filename)
    os.makedirs(output, exist_ok=True)

    # make folders "transcripcion", "srt", "questions", "opinion"
    os.makedirs(os.path.join(output, "transcripcion"), exist_ok=True)
    os.makedirs(os.path.join(output, "questions"), exist_ok=True)
    os.makedirs(os.path.join(output, "opinion"), exist_ok=True)

    if arguments.srt:
        os.makedirs(os.path.join(output, "srt"), exist_ok=True)
    os.makedirs(os.path.join(output), exist_ok=True)



    tp = TranscriptionProcessor(
        model_size=arguments.whisper_model,
        language='Spanish',
        num_speakers=2,
        speakers=None,
        local_mode=arguments.local
    )
    tc = TimeChecker()

    wav_path = tp.convert_to_wav(file)

    tc.start()    
    transcription = tp.transcribe(file)
    tiempo = tc.stop()


    transcript = f"{tiempo}\n\n"+transcription["text"]

    # Save transcript and srt
    tp.save_transcript(transcript, os.path.join(output, "transcripcion", f"{filename}.txt"))
    if arguments.srt:
        segments = tp.get_srt(wav_path, transcription["segments"])
        tp.save_transcript_srt(transcription["segments"], os.path.join(output, "srt", f"{filename}.srt"))

    response = llm.generate(transcription["text"])
    json_data = json.loads(response)

    # Preguntas
    question_file = f"Opinion: {json_data['opinion']}\n\n\n Questions:\n\n"
    for question in json_data["questions"]:
        question_file += f"- {question}\n\n"

    with open(os.path.join(output, "questions", f"{filename}-.txt"), "w") as f:
        f.write(question_file)



