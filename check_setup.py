import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("Setup OK: Gemini API key found.")
    print("Key starts with:", api_key[:4] + "...")
else:
    print("Problem: no GEMINI_API_KEY found. Check your .env file.")