from gtts import gTTS
import pygame
import os
import time

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait until playback is finished
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()

    try:
        os.remove(filename)
    except Exception as e:
        print(f"⚠️ Could not delete {filename}: {e}")
