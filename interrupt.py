import sounddevice as sd
import numpy as np
import queue
import threading

interrupt_event = threading.Event()

def detect_interrupt(threshold=0.02, chunk_size=1024, device=None):
    q = queue.Queue()

    def audio_callback(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > threshold:
            interrupt_event.set()
        q.put(indata.copy())

    with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000, blocksize=chunk_size, device=device):
        while True:
            q.get()

def start_interrupt_listener():
    thread = threading.Thread(target=detect_interrupt, daemon=True)
    thread.start()
