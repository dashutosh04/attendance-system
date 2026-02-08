import json, torch, time, random, os
import pandas as pd
import speech_recognition as sr
from datetime import date

from audio_utils import record_audio, beep, float_to_int16, has_speech
from speaker import get_embedding, similarity
from tts import speak
from logger import log

PHRASES = ["present sir", "yes sir present", "here sir"]
INTENT_WORDS = ["present", "yes", "here"]
MAX_ATTEMPTS = 3
os.makedirs("attendance_logs", exist_ok=True)

def sim_to_conf(sim):
    if sim < 0.5: return 0
    if sim > 0.85: return 100
    return int((sim - 0.5) / 0.35 * 100)

def run_attendance(update_ui, manual_cb, similarity_enabled=True):
    mode = "SPEECH + VOICE" if similarity_enabled else "SPEECH ONLY"
    log("MODE", "CONFIG", mode)
    update_ui(f"Mode: {mode}")

    students = json.load(open("students.json"))
    recog = sr.Recognizer()
    results = []

    for roll, path in students.items():
        data = torch.load(path)
        refs, threshold = data["embeddings"], data["threshold"]

        phrase = random.choice(PHRASES)
        speak(f"Roll ending {roll[-4:]}. Say {phrase}")
        update_ui(f"Calling ****{roll[-4:]}")
        log("ROLL", "CALL", roll)

        present = False
        final_sim = 0.0
        auto_decision_made = False

        for _ in range(MAX_ATTEMPTS):
            beep()
            audio = record_audio(3)

            if not has_speech(audio):
                log("AUDIO", "SILENCE", roll)
                continue

            try:
                pcm = float_to_int16(audio)
                text = recog.recognize_google(
                    sr.AudioData(pcm.tobytes(), 16000, 2)
                ).lower()
                log("STT", "OK", text)
            except:
                log("STT", "FAIL", roll)
                continue

            if similarity_enabled:
                live = get_embedding(audio)
                sim = max(similarity(live, r) for r in refs)
                final_sim = sim
                log("VOICE", "SIM", f"{sim:.2f}")

                if phrase in text and sim >= threshold:
                    present = True
                    auto_decision_made = True
                    log("VERIFY", "PASS", "Phrase + voice matched")
                    break
            else:
                if any(word in text for word in INTENT_WORDS):
                    present = True
                    auto_decision_made = True
                    log("VERIFY", "PASS", f"Speech intent: {text}")
                    break

        if not auto_decision_made:
            log("MANUAL", "REQUIRED", roll)
            present = manual_cb(roll)

        status = "Present" if present else "Absent"
        conf = sim_to_conf(final_sim)

        speak(status)
        log("ATTENDANCE", status.upper(), roll)
        results.append([roll, status, conf])
        time.sleep(0.4)

    csv = f"attendance_logs/attendance_{date.today()}.csv"
    pd.DataFrame(results, columns=["Roll","Status","Confidence"]).to_csv(csv, index=False)
    update_ui(f"Saved → {csv}")
    log("SYSTEM", "END", "Attendance complete")
