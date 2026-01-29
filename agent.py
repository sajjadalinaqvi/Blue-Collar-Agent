# agent.py

import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API endpoint from environment
API_URL = os.getenv("GULLU_API_URL", "http://localhost:8000/bluecollar")

def get_response(history):
    """
    Sends the conversation history to the backend API and gets assistant response.
    :param history: List of dicts with roles ("user"/"assistant") and "content".
    :return: Assistant's generated response string.
    """
    try:
        response = requests.post(API_URL, json={"history": history})
        response.raise_for_status()
        return response.json().get("assistant_response", "Sorry, I didn't catch that.")
    except Exception as e:
        print(f"[❌ ERROR] Failed to get response from API: {e}")
        return "Sorry, something went wrong while contacting the assistant."
