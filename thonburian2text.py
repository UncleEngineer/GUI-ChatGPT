import torch
from transformers import pipeline

MODEL_NAME = "biodatlab/whisper-th-medium-combined"  # see alternative model names below
lang = "th"

device = 0 if torch.cuda.is_available() else "cpu"

pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=30,
    device=device,
)

#  pass audio as quoted string "audio.wav"
def transcribe_text(audio):
    text = pipe(audio, generate_kwargs={"language":"<|th|>", "task" : "transcribe"}, batch_size=16)["text"]
    return(text)   

    '''
    with open("transcribed_text.txt","w") as file:
        file.write(text)
        '''
'''
# Perform ASR with the created pipe.
pipe("audio.mp3", generate_kwargs={"language":"<|th|>", "task":"transcribe"}, batch_size=16)["text"]
'''
