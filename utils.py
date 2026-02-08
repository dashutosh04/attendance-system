import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000

def record_audio(duration=3):
    print("Listening...")
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )
    sd.wait()
    return audio.flatten()
