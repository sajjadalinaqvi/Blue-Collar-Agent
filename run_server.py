from flask import Flask, request, render_template, jsonify
from datetime import datetime
import os
import tempfile
import whisper
from dotenv import load_dotenv

from agent import get_response
from tts import speak
from memory import update_history, load_history

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage, SystemMessage

# 🔄 Load environment variables
load_dotenv()

# 🌐 Initialize Flask app
app = Flask(__name__)

# 🎙️ Load Whisper model once
model = whisper.load_model("base")

# 📄 Load system prompt from prompt.txt
with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# 🤖 Initialize the Groq LLM
llm = ChatGroq(
    api_key=os.getenv("API_KEY"),
    model="llama3-70b-8192"
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
        result = model.transcribe(temp_path)
        user_text = result["text"].strip()
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

        response = llm(messages)
        return jsonify({"assistant_response": response.content})

    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({"assistant_response": "Sorry, I ran into a problem."}), 500


# ------------------ ENTRY POINT ------------------

if __name__ == "__main__":
    app.run(debug=True)
