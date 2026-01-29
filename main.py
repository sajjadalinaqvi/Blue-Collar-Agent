from stt import transcribe
from tts import speak
from agent import get_response
from memory import update_history, load_history
from interrupt import start_interrupt_listener, interrupt_event
import time
import subprocess
import sys

def start_server():
    """Start Flask server in background using virtual environment"""
    venv_python = "/home/datalytics-dev/sajjad/VOIP-projects/Blue-Collar-Agent/.venv/bin/python"
    return subprocess.Popen([venv_python, "run_server.py"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

def run_agent():
    print("🚀 Starting backend server...")
    server_process = start_server()
    time.sleep(5)  # Wait longer for server
    
    print("👂 Gullu is listening for your voice...")
    # Don't start interrupt listener until after first transcription
    
    history = load_history()

    try:
        while True:
            user_input = transcribe()
            if user_input:
                # Start interrupt listener only after we get valid input
                if not hasattr(run_agent, 'interrupt_started'):
                    start_interrupt_listener()
                    run_agent.interrupt_started = True
                    
                update_history("user", user_input)
                history = load_history()  # Reload history
                response = get_response(history)
                update_history("assistant", response)

                print(f"🗣️ You: {user_input}")
                print(f"🤖 Gullu: {response}")
                speak(response)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    finally:
        server_process.terminate()
        print("✅ Done")

if __name__ == "__main__":
    run_agent()
