import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL")

client = genai.Client(api_key=api_key)


def ask_ai(question):
    response = client.models.generate_content(
        model=model_name,
        contents=question,
    )
    return response.text


if __name__ == "__main__":
    question = input("Ask a question: ")
    start = time.time()
    answer = ask_ai(question)
    seconds = time.time() - start
    print("\nAnswer:", answer)
    print(f"\n(Took {seconds:.1f} seconds)")