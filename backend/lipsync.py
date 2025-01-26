import requests
import dotenv
from typing import Any
import re
import hashlib
import hmac
import json
import os

# Obtain environment variables
# env_vars = dotenv.dotenv_values()
env_vars = dict(os.environ)
URL = "https://api.sync.so/v2/generate"
API_KEY = env_vars['SYNC_API_KEY']
WEBHOOK_SECRET = env_vars['WEBHOOK_SECRET']
LIPSYNC_DEFAULT_VIDEO = env_vars['LIPSYNC_DEFAULT_VIDEO']
WEBHOOK_URL = env_vars['WEBHOOK_URL']

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

def generate_lipsync(tts_url: str):
    print("tts url:", tts_url)
    payload = {
        "model": "lipsync-1.7.1",
        "input": [
            {
                "type": "video",
                "url": LIPSYNC_DEFAULT_VIDEO
            },
            {
                "type": "audio",
                "url": tts_url
            }
        ],
        "options": {
            "pads": [0,5,0,0],
            "output_format": "mp4",
            "sync_mode": "loop",
            "active_speaker": False
        },
        "webhookUrl": WEBHOOK_URL
    }

    response = requests.request("POST", URL, json=payload, headers=headers)
    print(response.json())
    return response

"""
    Verifies the webhook signature of Sync's returned payload.
"""
def verify_signature(payload: Any, signature: str) -> bool:
    if not signature:
        return False

    try:
        match = re.match(r't=(\d+),v1=(.+)', signature)
        if not match:
            return False

        timestamp, received_signature = match.groups()
        if not timestamp or not received_signature:
            return False

        message = f"{timestamp}.{json.dumps(payload, separators=(',', ':'))}"

        expected_signature = hmac.new(
            WEBHOOK_SECRET.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        # Timing-safe comparison to prevent timing attacks
        return hmac.compare_digest(received_signature, expected_signature)
    except Exception:
        return False