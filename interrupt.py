import sounddevice as sd
import numpy as np
import queue
import threading
import time

interrupt_event = threading.Event()

def detect_interrupt(threshold=0.05, chunk_size=1024, device=None):
    q = queue.Queue()
    consecutive_loud = 0
    required_consecutive = 3  # Need 3 consecutive loud chunks

    def audio_callback(indata, frames, time, status):
        nonlocal consecutive_loud
        volume_norm = np.linalg.norm(indata) * 10
        
        if volume_norm > threshold:
            consecutive_loud += 1
            if consecutive_loud >= required_consecutive:
                interrupt_event.set()
                consecutive_loud = 0
        else:
            consecutive_loud = 0
            
        q.put(indata.copy())

    with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000, blocksize=chunk_size, device=device):
        while True:
            try:
                q.get(timeout=1)
            except:
                break

def start_interrupt_listener():
    thread = threading.Thread(target=detect_interrupt, daemon=True)
    thread.start()
