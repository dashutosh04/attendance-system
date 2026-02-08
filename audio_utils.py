import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 16000
sd.default.samplerate = SAMPLE_RATE

def beep():
    t = np.linspace(0, 0.18, int(SAMPLE_RATE * 0.18), False)
    tone = 0.4 * np.sin(2 * np.pi * 1000 * t)
    sd.play(tone, SAMPLE_RATE, blocking=True)
    sd.stop()
    time.sleep(0.15)

def record_audio(seconds=3):
    time.sleep(0.1)
    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocking=True
    )
    return audio.flatten()

def float_to_int16(audio):
    audio = np.clip(audio, -1.0, 1.0)
    return (audio * 32767).astype("int16")

def has_speech(audio, threshold=0.01):
    return float(abs(audio).mean()) > threshold
