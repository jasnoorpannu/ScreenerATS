import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()

print("\n=== AVAILABLE MODELS FOR YOUR KEY ===\n")
for m in models:
    print(m.name, " | Supported:", m.supported_generation_methods)
