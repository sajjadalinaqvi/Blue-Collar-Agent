from flask import Flask, request, render_template, jsonify
from datetime import datetime
import os
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from dotenv import load_dotenv

from agent import get_response
from tts import speak
from memory import update_history, load_history

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 🔄 Load environment variables
load_dotenv()

# 🌐 Initialize Flask app
app = Flask(__name__)

# 🎙️ Initialize speech recognizer
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

# 📄 Load system prompt from prompt.txt
with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# 🤖 Initialize the Groq LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

# ------------------ ROUTES ------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    temp_path = os.path.join(tempfile.gettempdir(), f"temp_{datetime.now().timestamp()}.wav")
    file.save(temp_path)

    try:
        # Convert audio to WAV format
        audio = AudioSegment.from_file(temp_path)
        wav_path = temp_path.replace('.wav', '_converted.wav')
        audio.export(wav_path, format="wav")
        
        # Use Google Speech Recognition
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            user_text = recognizer.recognize_google(audio_data, language='en-US')
            
        # Clean up converted file
        try:
            os.remove(wav_path)
        except:
            pass
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return jsonify({"error": "Failed to transcribe audio"}), 500
    finally:
        try:
            os.remove(temp_path)
        except Exception as e:
            print(f"⚠️ Could not delete temp file: {e}")

    if user_text:
        update_history("user", user_text)
        history = load_history()
        assistant_response = get_response(history)
        update_history("assistant", assistant_response)

        speak(assistant_response)

        return jsonify({
            "user": user_text,
            "assistant": assistant_response
        })

    return jsonify({"error": "Empty transcription"}), 500


@app.route("/bluecollar", methods=["POST"])
def bluecollar_agent():
    try:
        data = request.json
        history = data.get("history", [])

        # 🧠 Build message chain with system prompt
        messages = [SystemMessage(content=system_prompt)]
        for turn in history:
            role = turn.get("role")
            content = turn.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))

        response = llm.invoke(messages)
        return jsonify({"assistant_response": response.content})

    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({"assistant_response": "Sorry, I ran into a problem."}), 500


# ------------------ ENTRY POINT ------------------

if __name__ == "__main__":
    print("🌍 Starting Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
