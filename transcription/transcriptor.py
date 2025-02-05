from progress.bar import ChargingBar
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
import os
import sys
import tempfile
# from rich import print
from config import WHISPER_MODEL , FRAGMENT_DURATION, DEVICE, LOCAL_MODE, MODEL_API_KEY

if LOCAL_MODE:
    import whisper #type: ignore
else:
    from openai import OpenAI
    from openai.types.audio import Transcription

class Transcriptor:
    def __init__(self, initial_prompt=""):
        self.initial_prompt = initial_prompt
        self.device_type = DEVICE
        if LOCAL_MODE:
            self.whisper = whisper.load_model(WHISPER_MODEL, self.device_type)
        else:
            self.whisper = OpenAI(
                api_key=MODEL_API_KEY
            )
        self.temp_dir = tempfile.mkdtemp()
    
    def extract_audio(self, video_path) -> VideoFileClip:
        return VideoFileClip(video_path).audio
    
    def fragment_audio(self, audio) -> list[str]:
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
            bar.start()
            for fragment_path in fragment_files:
                if LOCAL_MODE: 
                    result = self.whisper.transcribe(fragment_path, initial_prompt=f"{self.initial_prompt}, el podcast es chileno")
                    text_transcription.append(result["text"])
                else:
                    file = open(fragment_path, "rb")
                    result:Transcription = self.whisper.audio.transcriptions.create(
                        model="whisper-1",
                        file=file,
                    )

                    text_transcription.append(result.text)
                bar.next()
            bar.finish()
            return text_transcription
        finally:
            pass
