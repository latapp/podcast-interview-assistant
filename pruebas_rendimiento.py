import json
from LLM.llm import LLM
import os
from transcriptor_srt.transcriptor_processor import TranscriptionProcessor
from utils.time_checker import TimeChecker


llm = LLM()

base_output = "./output"
file = os.path.join("./tests", "juanjo_montecinos.mp3")
filename = os.path.basename(file).split(".")[0]
output = os.path.join(base_output, filename)
os.makedirs(output, exist_ok=True)

# make folders "transcripcion", "srt", "questions", "opinion"
os.makedirs(os.path.join(output, "transcripcion"), exist_ok=True)
os.makedirs(os.path.join(output, "srt"), exist_ok=True)
os.makedirs(os.path.join(output, "questions"), exist_ok=True)
os.makedirs(os.path.join(output, "opinion"), exist_ok=True)



os.makedirs(os.path.join(output), exist_ok=True)


tiempo = {
    "turbo":"",
    "large":""
}
tests = ["turbo","large"]


for test in tests:
    tp = TranscriptionProcessor(
        model_size='turbo',
        language='Spanish',
        num_speakers=2,
        speakers=None,
        local_mode=test=="turbo"
    )
    tc = TimeChecker()
    wav_path = tp.convert_to_wav(file)

    tc.start()    
    transcription = tp.transcribe(file)
    tiempo = tc.stop()


    transcript = f"{tiempo}\n\n"+transcription["text"]
    tp.save_transcript(transcript, os.path.join(output, "transcripcion", f"{filename}-{test}.txt"))
    tp.save_transcript_srt(transcription["segments"], os.path.join(output, "srt", f"{filename}-{test}.srt"))

    response = llm.generate(transcription["text"])
    json_data = json.loads(response)

    question_file = f"Opinion: {json_data['opinion']}\n\n\n Questions:\n\n"
    for question in json_data["questions"]:
        question_file += f"- {question}\n\n"
    with open(os.path.join(output, "questions", f"{filename}-{test}.txt"), "w") as f:
        f.write(question_file)
    
    

