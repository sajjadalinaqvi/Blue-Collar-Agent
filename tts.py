import requests
import pygame
import os
import time
import io
from dotenv import load_dotenv
from interrupt import interrupt_event

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # George voice (free)

def speak(text):
    """Generate speech using Eleven Labs TTS with interruption support"""
    if not ELEVENLABS_API_KEY:
        print("❌ ELEVENLABS_API_KEY not found in environment")
        return
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_turbo_v2_5",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Save audio to temporary file
        filename = "temp_elevenlabs.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        
        # Play audio with interruption support
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Check for interruption while playing
        while pygame.mixer.music.get_busy():
            if interrupt_event.is_set():
                pygame.mixer.music.stop()
                interrupt_event.clear()
                print("🛑 Speech interrupted")
                break
            time.sleep(0.1)
        
        pygame.mixer.quit()
        
        # Clean up temp file
        try:
            os.remove(filename)
        except Exception as e:
            print(f"⚠️ Could not delete {filename}: {e}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Eleven Labs API error: {e}")
    except Exception as e:
        print(f"❌ TTS error: {e}")