import os
import tempfile
from tkinter.filedialog import Open
import whisper
import datetime
import subprocess
from moviepy.editor import AudioFileClip
import torch
import wave
from openai import OpenAI
import contextlib
import numpy as np

import config

class TranscriptionProcessor:
    def __init__(self, model_size='large', language='Spanish', num_speakers=2, speakers:list[str] = None, initial_prompt="",local_mode=config.LOCAL_MODE):
        self.initial_prompt = initial_prompt
        self.local_mode = local_mode
        self.speakers = speakers
        self.model_size = model_size
        self.language = language
        self.num_speakers = num_speakers
        self.temp_dir = tempfile.mkdtemp()
        self.setup_whisper_model()

    # Inicializa el modelo de embedding para reconocimiento de hablantes
    def setup_embedding_model(self):
        from pyannote.audio import Audio #type: ignore
        from pyannote.core import Segment #type: ignore
        from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding #type: ignore
        from sklearn.cluster import AgglomerativeClustering #type: ignore

        self.audio = Audio()
        self.embedding_model = PretrainedSpeakerEmbedding(
            "speechbrain/spkrec-ecapa-voxceleb",
            device=torch.device("cuda")
        )

    # Configura el modelo de Whisper según el idioma y tamaño
    def setup_whisper_model(self):
        if self.local_mode:
            self.model = whisper.load_model(self.model_size, device="cuda")
        else:
            self.model = OpenAI(
                api_key=config.MODEL_API_KEY,
                base_url=config.MODEL_BASE_URL
            )

    # Convierte el archivo de entrada a WAV si es necesario
    def convert_to_wav(self, input_path):
        try:
            if input_path.lower().endswith('.wav'):
                return input_path
            output_path = 'audio.wav'
            subprocess.call(['ffmpeg', '-i', input_path,"-ac","1", output_path, '-y'])
            return output_path
            
        except subprocess.CalledProcessError as e:
            print(f"[Error convert_to_wav] No se pudo convertir el archivo {input_path} a WAV. {e}")
            raise

    # Obtiene la duración del archivo de audio
    def get_audio_duration(self, wav_path):
        try:
            with contextlib.closing(wave.open(wav_path, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                return frames / float(rate)
        except wave.Error as e:
            print(f"[Error get_audio_duration] Problema al leer la duración de {wav_path}. {e}")
            raise

    # Genera embedding para un segmento de audio
    def segment_embedding(self, segment, audio_path, duration):
        start = segment["start"]
        end = min(duration, segment["end"])
        clip = Segment(start, end) #type: ignore
        waveform, _ = self.audio.crop(audio_path, clip)
        return self.embedding_model(waveform[None])


    def fragment_audio(self, audio) -> list[str]:
        """
        fragmenta el audio en fragmentos de maximo 20 segundos y los guarda temporalmente
        """
        audio_duration = audio.duration
        print(f"Duracion del audio: {int(audio_duration/60)} minutos y {int(audio_duration%60)} segundos")
        fragment_files = []
        start = 0
        fragment_duration = config.FRAGMENT_DURATION
        
        while start < audio_duration:
            end = min(start + fragment_duration, audio_duration)
            fragment = audio.subclip(start, end)
            
            # Guardar fragmento en archivo temporal
            temp_path = os.path.join(self.temp_dir, f"fragment_{start}.wav")
            fragment.write_audiofile(temp_path, fps=16000, nbytes=2, codec='pcm_s16le',verbose=False, logger=None)
            fragment_files.append(temp_path)
            start = end
            
        return fragment_files
    def transcribe(self, wav_path):
            if self.local_mode:
                return self.model.transcribe(wav_path,initial_prompt=self.initial_prompt)
            else:
                segments_files = self.fragment_audio(AudioFileClip(wav_path))
                transcription = ""
                segments = []

                for segment_file in segments_files:
                    file = open(segment_file, "rb")
                    response = self.model.audio.transcriptions.create(
                        model="whisper-1",
                        file=file,
                        prompt=self.initial_prompt,
                        timestamp_granularities=["segment"],
                        response_format="verbose_json"
                    )
                    response = response.model_dump()
                    transcription += response["text"]
                    segments += response["segments"]
                    file.close()
                
                return {
                    "text": transcription,
                    "segments": segments
                }
    def cleanup(self):
        try:
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
            os.rmdir(self.temp_dir)
        except Exception as e:
            print(f"[Error cleanup] Falla al limpiar archivos temporales. {e}")
            raise
    # Procesa el archivo de audio completo
    def get_srt(self, wav_path, segments):
        try:
            self.setup_embedding_model()
            
            duration = self.get_audio_duration(wav_path)
            
            # Generación de embeddings
            embeddings = np.zeros(shape=(len(segments), 192))
            for i, segment in enumerate(segments):
                embeddings[i] = self.segment_embedding(segment, wav_path, duration)
            
            # Clustering de hablantes
            embeddings = np.nan_to_num(embeddings)
            clustering = AgglomerativeClustering(self.num_speakers).fit(embeddings) #type: ignore
            
            # Asignación de hablantes
            for i, segment in enumerate(segments):
                if self.speakers and self.speakers[clustering.labels_[i]]:
                    segment["speaker"] = self.speakers[clustering.labels_[i]]
                else:
                    segment["speaker"] = f'SPEAKER {clustering.labels_[i] + 1}'
            
        except Exception as e:
            print(f"[Error process_audio] Falla procesando el archivo {wav_path}. {e}")
            raise
        
        return segments

    # Formatea el tiempo en formato legible
    def format_time(self, seconds):
        return datetime.timedelta(seconds=round(seconds))

    # Crea el diccionario de hablantes
    def create_speakers_dict(self, segments):
        if self.speakers:
            return {f'SPEAKER {i + 1}': speaker for i, speaker in enumerate(self.speakers)}


    def save_transcript(self, text, output_file="transcript.txt"):
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(text)

    # Guarda la transcripción con los hablantes en un archivo
    def save_transcript_with_speakers(self, segments, output_file="transcript.txt"):
        speaker_dict = self.create_speakers_dict(segments)
        with open(output_file, "w", encoding='utf-8') as f:
            for segment in segments:
                speaker = speaker_dict[segment['speaker']]
                start_time = self.format_time(segment['start'])
                text = segment["text"].strip()
                f.write(f"{speaker} {start_time}: {text}\n")
    
    def save_transcript_srt(self, segments, output_file="transcript.srt"):
    # Guarda la transcripción en un archivo SRT

        with open(output_file, "w", encoding='utf-8') as f:
            for i, segment in enumerate(segments):
                start_time = self.format_time(segment['start'])
                end_time = self.format_time(segment['end'])
                text = segment["text"].strip()
                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
