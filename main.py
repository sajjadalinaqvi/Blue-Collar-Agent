from stt import transcribe
from tts import speak
from agent import get_response
from memory import update_history, load_history
from interrupt import start_interrupt_listener, interrupt_event
import time

def run_agent():
    print("👂 Gullu is listening for your voice...")
    start_interrupt_listener()
    
    history = load_history()

    while True:
        user_input = transcribe()
        if user_input:
            update_history("user", user_input)
            response = get_response(history)
            update_history("assistant", response)

            print(f"🗣️ You: {user_input}")
            print(f"🤖 Gullu: {response}")
            speak(response)  # TTS auto-interrupts if interrupt_event is set

if __name__ == "__main__":
    run_agent()
