import sounddevice as sd
import soundfile as sf
import pygame
import numpy as np
import threading
import time
import queue

# Audio recording settings
SAMPLE_RATE = 44100
CHANNELS = 1
DURATION = 10  # fallback max duration if needed
FILENAME = "recorded.wav"

# Queue to handle recording state
recording_queue = queue.Queue()

def interrupt_tts():
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def record_audio():
    """Interrupt TTS and start recording immediately."""
    interrupt_tts()
    print("🎤 Recording started...")

    recording_queue.queue.clear()  # clear any old signal
    recording_queue.put("start")

    audio_data = []

    def callback(indata, frames, time, status):
        if status:
            print(f"Recording status: {status}")
        audio_data.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
        start_time = time.time()
        while True:
            if not recording_queue.empty() and recording_queue.get() == "stop":
                break
            if time.time() - start_time > DURATION:
                print("⏱️ Max duration reached.")
                break
            time.sleep(0.1)

    # Convert list of chunks to numpy array
    audio_np = np.concatenate(audio_data, axis=0)

    # Save to WAV
    sf.write(FILENAME, audio_np, SAMPLE_RATE)
    print("✅ Recording finished and saved.")
    return FILENAME

def stop_recording():
    """Signal to stop recording."""
    recording_queue.put("stop")
