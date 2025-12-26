import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API with environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
try:
    print("Available models:")
    for model in genai.list_models():
        print(f"- {model.name}")
        print(f"  - Supported generation methods: {model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"Error listing models: {e}")