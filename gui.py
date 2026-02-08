import customtkinter as ctk
from threading import Thread
from attendance_core import run_attendance
from enroll_core import enroll_student
import matplotlib.pyplot as plt
import pandas as pd
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Voice Attendance")
        self.geometry("950x650")

        self.manual_choice = None
        self.sim_enabled = ctk.BooleanVar(value=True)
        self.status = ctk.StringVar(value="Ready")

        ctk.CTkLabel(self, text="🎤 AI Voice Attendance",
                     font=ctk.CTkFont(size=26, weight="bold")).pack(pady=20)

        ctk.CTkLabel(self, textvariable=self.status,
                     font=ctk.CTkFont(size=18)).pack()

        ctk.CTkSwitch(self, text="Enable Voice Similarity",
                      variable=self.sim_enabled).pack(pady=5)

        self.roll_entry = ctk.CTkEntry(self, placeholder_text="Roll Number")
        self.roll_entry.pack(fill="x", padx=40, pady=10)

        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack()

        ctk.CTkButton(btns, text="Enroll",
                      command=self.enroll).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="Start Attendance",
                      command=self.start).pack(side="left", padx=10)
        ctk.CTkButton(btns, text="Confidence Graph",
                      command=self.graph).pack(side="left", padx=10)

        man = ctk.CTkFrame(self, fg_color="transparent")
        man.pack(pady=5)
        ctk.CTkButton(man, text="✔ Present",
                      command=lambda: self.set_manual(True)).pack(side="left", padx=10)
        ctk.CTkButton(man, text="✖ Absent",
                      command=lambda: self.set_manual(False)).pack(side="left", padx=10)

        self.log = ctk.CTkTextbox(self, height=300, font=("Consolas", 11))
        self.log.pack(fill="both", expand=True, padx=20, pady=20)

    def update_ui(self, msg):
        self.status.set(msg)
        self.log.insert("end", msg + "\n")
        self.log.see("end")

    def set_manual(self, v):
        self.manual_choice = v

    def manual_decision(self, roll):
        self.update_ui(f"Manual decision needed for {roll}")
        while self.manual_choice is None:
            pass
        v = self.manual_choice
        self.manual_choice = None
        return v

    def enroll(self):
        r = self.roll_entry.get().strip()
        if r:
            Thread(target=enroll_student, args=(r, self.update_ui), daemon=True).start()

    def start(self):
        Thread(
            target=run_attendance,
            args=(self.update_ui, self.manual_decision, self.sim_enabled.get()),
            daemon=True
        ).start()

    def graph(self):
        files = sorted(os.listdir("attendance_logs"))
        if not files: return
        df = pd.read_csv(f"attendance_logs/{files[-1]}")
        plt.bar(df["Roll"], df["Confidence"])
        plt.title("Confidence Graph")
        plt.show()

if __name__ == "__main__":
    App().mainloop()
