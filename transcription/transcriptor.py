from progress.bar import ChargingBar
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
import whisper
import numpy as np
import os
import sys
import tempfile
# from rich import print
from config import WHISPER_MODEL , FRAGMENT_DURATION, DEVICE

class Transcriptor:
    def __init__(self, initial_prompt=""):
        self.initial_prompt = initial_prompt
        self.device_type = DEVICE
        self.whisper = whisper.load_model(WHISPER_MODEL, self.device_type)
        self.temp_dir = tempfile.mkdtemp()
    
    def extract_audio(self, video_path) -> VideoFileClip:
        return VideoFileClip(video_path).audio
    
    def fragment_audio(self, audio):
        """
        fragmenta el audio en fragmentos de maximo 20 segundos y los guarda temporalmente
        """
        audio_duration = audio.duration
        print(f"Duracion del audio: {int(audio_duration/60)} minutos y {int(audio_duration%60)} segundos")
        fragment_files = []
        start = 0
        fragment_duration = FRAGMENT_DURATION
        
        while start < audio_duration:
            end = min(start + fragment_duration, audio_duration)
            fragment = audio.subclip(start, end)
            
            # Guardar fragmento en archivo temporal
            temp_path = os.path.join(self.temp_dir, f"fragment_{start}.wav")
            fragment.write_audiofile(temp_path, fps=16000, nbytes=2, codec='pcm_s16le',verbose=False, logger=None)
            fragment_files.append(temp_path)
            start = end
            
        return fragment_files

    def cleanup(self):
        """Limpia los archivos temporales"""
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def transcribe(self, path_file):
        try:
            if not os.path.exists(path_file):
                print(f"El archivo {path_file} no existe")
                sys.exit(1)
            if path_file.endswith(".mp4"):
                print("El archivo es un video")
                audio = self.extract_audio(path_file)
            else:
                print("El archivo es un audio")
                audio = AudioFileClip(path_file)

            fragment_files = self.fragment_audio(audio)
            print(f"Fragmentos generados: {len(fragment_files)}")
            text_transcription = []
            bar = ChargingBar("Transcribiendo fragmentos", max=len(fragment_files))
            for fragment_path in fragment_files:
                result = self.whisper.transcribe(fragment_path, initial_prompt=f"{self.initial_prompt}, el podcast es chileno")
                text_transcription.append(result["text"])
                bar.next()
            return text_transcription
        finally:
            self.cleanup()

if __name__ == "__main__":
    transcriptor = Transcriptor()
    result = transcriptor.transcribe("transcription/bernardita-ruffineli---klein-podcast-1.mp4")
    print(result)