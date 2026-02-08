import pyttsx3
import time
import re

DIGIT_MAP = {
    '0':'zero','1':'one','2':'two','3':'three','4':'four',
    '5':'five','6':'six','7':'seven','8':'eight','9':'nine'
}

def _normalize_numbers(text):
    def repl(m): return " ".join(DIGIT_MAP[d] for d in m.group())
    return re.sub(r'\d+', repl, text)

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)
    engine.setProperty("volume", 1.0)

    for v in engine.getProperty("voices"):
        if "zira" in v.name.lower() or "female" in v.name.lower():
            engine.setProperty("voice", v.id)
            break

    engine.say(_normalize_numbers(str(text)))
    engine.runAndWait()
    engine.stop()
    time.sleep(0.2)
