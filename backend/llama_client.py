import os
import requests
import logging
from dotenv import load_dotenv

from pathlib import Path
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
LLAMA_API_URL = os.getenv("LLAMA_API_URL", "https://api.groq.com/openai/v1/chat/completions")
MODEL_NAME = os.getenv("LLAMA_MODEL", "llama-3.1-8b-instant")

if not LLAMA_API_KEY:
    raise ValueError("Missing API key. Please set LLAMA_API_KEY in .env file.")

logging.basicConfig(level=logging.INFO)

def query_llama(prompt: str) -> str:
    """
    Sends a prompt to Groq LLaMA API and returns the AI-generated text.
    """
    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are Secure Chat Guardian — a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 256
    }

    try:
        response = requests.post(LLAMA_API_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        raise RuntimeError("⚠️ LLaMA API request timed out.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"❌ LLaMA API request failed: {e}")
    except (KeyError, IndexError):
        raise RuntimeError("⚠️ Unexpected response format from LLaMA API.")