import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile

model = whisper.load_model("base")

def transcribe(duration=10):
    print("🎤 Listening...")
    fs = 16000
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        wav.write(tmp.name, fs, audio)
        result = model.transcribe(tmp.name)
        return result["text"].strip()
