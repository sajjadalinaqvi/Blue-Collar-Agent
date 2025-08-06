# Real-Time Voice Assistant for Blue-Collar Services

This Agent is a local, real-time voice assistant designed to help users schedule and manage blue-collar services like electricians, plumbers, and cleaners. It runs locally using a Flask server and provides intelligent conversational support with memory, barge-in interruption, and real-time response capabilities.

---

## 🧠 Features

- 🔊 Real-time speech-to-text using OpenAI Whisper
- 🗣️ Offline Text-to-Speech with smooth chunked playback and barge-in detection
- 🧾 Conversation memory logging to JSON
- 📞 Handles voice interruptions with `webrtcvad`
- 🌐 Backend integration with `/bluecollar` API
- 💡 Custom assistant logic for service booking and customer support

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2.Runt the Voice Assistant
```bash
python main.py
```
### 3. (Optional) Launch Web UI

```bash
python run_server.py
```
Then open http://localhost:5000 in your browser.

---


## ⚙️ Configuration
Create a .env file with your API endpoint:
```bash
GULLU_API_URL=http://localhost:8000/bluecollar
```

---

## 📋 Requirements
Python 3.10+

FFmpeg (for Whisper + TTS)

Whisper model (base/medium preferred)

Optional: Chrome (for UI frontend)

---


## 📌 Use Cases
📅 Book plumbers, electricians, AC technicians

🧠 Retain customer name, job type, and appointment

🛑 Interrupt ongoing voice output naturally

---


## 🤖 Backend Agent Requirements

The voice assistant expects a REST API at /bluecollar that responds to this format:
```bash
{
  "user_query": "...",
  "history": [...],
  "timestamp": "...",
  "assistant_response": "..."
}
```




