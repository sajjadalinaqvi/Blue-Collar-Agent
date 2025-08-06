import json
from datetime import datetime

LOG_FILE = "conversation_log.json"

def load_history():
    try:
        with open(LOG_FILE, 'r') as f:
            return json.load(f)["history"]
    except:
        return []

def update_history(role, content):
    data = {"timestamp": str(datetime.now()), "role": role, "content": content}
    try:
        with open(LOG_FILE, 'r') as f:
            log = json.load(f)
    except:
        log = {"history": []}
    log["history"].append(data)
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)
