from datetime import datetime

LOG_FILE = "attendance.log"

def log(action, status, message):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] | {action:<16} | {status:<10} | {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
