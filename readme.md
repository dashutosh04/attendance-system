# AI-Based Voice Attendance System

**Type:** Minor Project

**Domain:** Artificial Intelligence, Speech Processing, Biometrics

## 1. Introduction

Traditional attendance systems are time-consuming, error-prone, and vulnerable to proxy attendance.
This project proposes an **AI-based automated attendance system** that uses
**speech intent detection** and **speaker recognition** to mark attendance.

The system announces roll numbers, listens for student responses, verifies identity using voice biometrics,
and records attendance automatically with manual override support.

## 2. Objectives

- Automate attendance marking using voice
- Prevent proxy attendance using speaker recognition
- Provide fallback manual control for instructors
- Maintain explainable confidence scores
- Generate date-wise attendance records

## 3. System Architecture

The system is modular and consists of the following components:

| Module | Description |
|--------|-------------|
| GUI | User interface for enrollment, attendance, and monitoring |
| Audio Module | Handles microphone input and beep signals |
| TTS Module | Announces roll numbers and system responses |
| Speaker Recognition | Verifies speaker identity using AI |
| Speech Recognition | Detects spoken words like "present" |
| Logging System | Tracks system events for transparency |

## 4. Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python | Main programming language |
| SpeechBrain | Speaker recognition (ECAPA-TDNN) |
| SpeechRecognition | Speech-to-text (intent detection) |
| pyttsx3 | Offline text-to-speech |
| sounddevice | Microphone audio capture |
| CustomTkinter | Modern GUI |
| Pandas | CSV generation |

## 5. Speaker Recognition Model

The system uses a **pretrained ECAPA-TDNN model** from SpeechBrain.
This model converts voice audio into fixed-length numerical vectors called *speaker embeddings*.

> **Model Name:** ECAPA-TDNN (trained on VoxCeleb dataset)  
> **Purpose:** Identify who is speaking, not what is spoken

Speaker identity is verified by computing **cosine similarity** between live and enrolled embeddings.

## 6. Speech Recognition (Intent Detection)

Speech-to-text is used only to detect **intent**, not identity.
Accepted intent words include:

