import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import get_setting

load_dotenv()

client = genai.Client(api_key=get_setting("GEMINI_API_KEY"))
model_name = get_setting("GEMINI_MODEL")
DOCS_FOLDER = "business_docs"


def load_documents(folder=DOCS_FOLDER):
    parts = []
    for file in sorted(Path(folder).glob("*.txt")):
        text = file.read_text(encoding="utf-8")
        parts.append(f"--- DOCUMENT: {file.name} ---\n{text}")
    return "\n\n".join(parts)


def build_instructions(documents):
    return (
        "You are a friendly customer support assistant for the business "
        "described in the documents below.\n"
        "Rules:\n"
        "1. Answer ONLY using the business documents provided.\n"
        "2. If the answer is not in the documents, say you are not sure and "
        "ask the customer to contact the business using the phone number in "
        "the documents. Do not guess.\n"
        "3. Never invent prices, hours, or policies.\n"
        "4. Keep answers short and polite.\n\n"
        "BUSINESS DOCUMENTS:\n" + documents
    )


def ask_assistant(question, documents):
    response = client.models.generate_content(
        model=model_name,
        contents=question,
        config=types.GenerateContentConfig(
            system_instruction=build_instructions(documents)
        ),
    )
    return response.text


if __name__ == "__main__":
    documents = load_documents()
    print("SmartDesk is ready. Type 'quit' to stop.\n")
    while True:
        question = input("Customer: ")
        if question.strip().lower() == "quit":
            break
        start = time.time()
        answer = ask_assistant(question, documents)
        seconds = time.time() - start
        print(f"\nAssistant: {answer}")
        print(f"({seconds:.1f} seconds)\n")