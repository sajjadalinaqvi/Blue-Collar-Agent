from RealtimeSTT import AudioToTextRecorder
import threading
import time
from interrupt import interrupt_event

def transcribe():
    """Real-time transcription with barge-in support"""
    print("🎤 Listening...")
    
    try:
        # Initialize recorder for each transcription
        recorder = AudioToTextRecorder(
            model="base",
            language="en",
            silero_sensitivity=0.4,
            webrtc_sensitivity=2,
            post_speech_silence_duration=1.0,
            min_length_of_recording=1.0,
            min_gap_between_recordings=0,
            enable_realtime_transcription=False,
        )
        
        # Start recording and wait for completion
        recorder.start()
        
        # Simple wait for completion without interrupt checking during initial recording
        while recorder.is_recording:
            time.sleep(0.1)
            
        # Get the transcribed text
        text = recorder.text()
        return text.strip() if text else ""
        
    except Exception as e:
        print(f"❌ STT Error: {e}")
        return ""
    finally:
        try:
            if hasattr(recorder, 'is_recording') and recorder.is_recording:
                recorder.stop()
        except:
            pass
