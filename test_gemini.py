import os
import traceback

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

print("API key loaded:", bool(api_key))
print("API key length:", len(api_key))
print("Model:", model)

client = genai.Client(api_key=api_key)

try:
    print("\nConnecting to Gemini...")

    response = client.models.generate_content(
        model=model,
        contents="Reply with exactly: Gemini connection successful"
    )

    print("\nGemini response:")
    print(response.text)

except Exception as error:
    print("\nGemini request failed!")
    print("Exception type:", type(error).__name__)
    print("Exception:", repr(error))

    traceback.print_exc()

finally:
    client.close()