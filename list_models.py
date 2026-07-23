import os
import sys

# Forzar UTF-8 en stdout para Windows
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
import anthropic
client = anthropic.Anthropic(api_key=api_key)

try:
    response = client.models.list()
    print("Available models:")
    for model in response.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"Error fetching models: {e}")
