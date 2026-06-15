from dotenv import load_dotenv
import os
import logging

# Load environment variables
from pathlib import Path
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
LLAMA_API_URL = os.getenv("LLAMA_API_URL", "https://api.groq.com/openai/v1/chat/completions")

if not LLAMA_API_KEY:
    raise ValueError("Missing API key. Please set LLAMA_API_KEY in .env file.")

if not LLAMA_API_URL:
    print("⚠️ Warning: LLAMA_API_URL not set. Using default Groq endpoint.")

logging.basicConfig(level=logging.INFO)

_all_ = ["LLAMA_API_KEY", "LLAMA_API_URL"]