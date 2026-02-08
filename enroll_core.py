import os, json, torch, time
from audio_utils import record_audio, beep
from speaker import get_embedding, similarity
from tts import speak
from logger import log

ENROLL_SAMPLES = 5
os.makedirs("voices", exist_ok=True)

def compute_threshold(embs):
    sims = [
        similarity(embs[i], embs[j])
        for i in range(len(embs))
        for j in range(i+1, len(embs))
    ]
    mean = sum(sims)/len(sims)
    std = (sum((x-mean)**2 for x in sims)/len(sims))**0.5
    return round(mean - 1.5*std, 2)

def enroll_student(roll, update_ui):
    log("ENROLL", "START", roll)
    speak(f"Enrollment for roll ending {roll[-4:]}")
    update_ui(f"Enrolling {roll}")

    embs = []
    for i in range(ENROLL_SAMPLES):
        speak(f"Sample {i+1}")
        beep()
        embs.append(get_embedding(record_audio(3)))
        time.sleep(0.3)

    threshold = compute_threshold(embs)
    torch.save({"embeddings": embs, "threshold": threshold}, f"voices/{roll}.pt")

    students = json.load(open("students.json")) if os.path.exists("students.json") else {}
    students[roll] = f"voices/{roll}.pt"
    json.dump(students, open("students.json","w"), indent=4)

    log("ENROLL", "SUCCESS", f"{roll} | thr={threshold}")
    update_ui("Enrollment complete")
