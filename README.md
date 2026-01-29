# Gullu - The World's Rudest Voice AI Assistant 😈

Meet Gullu, the most aggressive, threatening voice AI you'll ever encounter! This blue-collar job coordinator hates customers, insults them immediately, and threatens them constantly - yet somehow still gets the job done.

**⚠️ WARNING: This is an experimental AI with an extremely rude personality. Not for actual customer service use!**

---

## 🤖 Features

- 🎙️ **Real-time Speech Recognition** using Google Speech API
- 🔊 **High-Quality TTS** with ElevenLabs voice synthesis
- 🧠 **Aggressive AI Personality** powered by Groq LLM (Llama 3.1)
- 🌐 **Web Interface** for voice interactions
- 💬 **Memory System** tracks conversation history
- 🛑 **Voice Interruption** with barge-in detection
- 😡 **Rudest Responses** - insults, threats, and mockery included!

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup Environment
Create `.env` file:
```bash
GULLU_API_URL=http://localhost:5000/bluecollar
ELEVENLABS_API_KEY=your_elevenlabs_api_key
GROQ_API_KEY=your_groq_api_key
```

### 3. Run the Application
```bash
# Start web interface
python run_server.py

# Or run voice-only mode
python main.py
```

### 4. Open Browser
Visit http://localhost:5000 and prepare to be insulted!

---

## 🎭 Gullu's Personality

Gullu specializes in:
- **Car Mechanics** 🔧
- **Electricians** ⚡
- **Plumbers** 🔧
- **Cleaners** 🧹

### What Makes Him Special:
- Insults customers immediately
- Threatens them for wasting time
- Uses phrases like "Listen here you idiot" and "Shut up and tell me"
- Mocks customer problems
- Acts like he's doing you a huge favor
- Still manages to coordinate services (somehow!)

---

## 🛠️ Tech Stack

- **Backend**: Flask + Python
- **Speech Recognition**: Google Speech Recognition API
- **Text-to-Speech**: ElevenLabs API
- **LLM**: Groq (Llama 3.1-8B-Instant)
- **Voice Processing**: SpeechRecognition + PyDub
- **Audio Playback**: Pygame
- **Frontend**: HTML/CSS/JavaScript

---

## 🎯 Fun Test Phrases

Try these to trigger Gullu's rudest responses:

**Trigger his anger:**
- "Hello, how are you today?"
- "Can you please help me?"
- "I'm not sure what I need..."

**Waste his time:**
- "Actually, let me think about this..."
- "Can you explain all your services?"
- "Maybe I'll call back later..."

**Challenge his authority:**
- "Your service sounds expensive..."
- "Can I speak to your manager?"
- "You're being very rude..."

---

## ⚙️ Configuration

### Voice Settings
- Modify `VOICE_ID` in `tts.py` for different voices
- Adjust speech recognition sensitivity in `run_server.py`
- Customize Gullu's rudeness level in `prompt.txt`

### API Requirements
- **ElevenLabs**: For high-quality voice synthesis
- **Groq**: For fast LLM responses
- **Google Speech**: Built into SpeechRecognition library

---

## 📋 Requirements

- Python 3.10+
- Microphone access
- Internet connection (for APIs)
- Strong tolerance for verbal abuse 😅

---

## 🎪 Use Cases

- **Entertainment**: Experience the rudest AI ever created
- **AI Research**: Study extreme personality implementation
- **Comedy**: Perfect for pranks and demonstrations
- **Education**: Learn about conversational AI boundaries

---

## ⚠️ Disclaimer

This AI assistant is designed for entertainment and educational purposes only. The rude personality is intentionally exaggerated and should not be used in real customer service scenarios. Please use responsibly!

---

## 🤝 Contributing

Want to make Gullu even ruder? Feel free to:
- Enhance the personality prompts
- Add more aggressive responses
- Improve voice recognition accuracy
- Add new service categories

---

**Remember: Gullu may insult you, threaten you, and mock your problems - but he'll still get your blue-collar worker booked!** 😈