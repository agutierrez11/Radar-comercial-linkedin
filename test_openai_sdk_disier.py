import sys
from openai import OpenAI

sys.stdout.reconfigure(encoding='utf-8')

client = OpenAI(
    base_url="https://llm.disier.net/v1",
    api_key="sk-0MINhr9-vEmzYLUFx-OvjQ"
)

print("--- PROBANDO CON OPENAI SDK OFICIAL ---", flush=True)

try:
    response = client.chat.completions.create(
        model="Qwen/Qwen3.8-27B",
        messages=[
            {"role": "user", "content": "Genera 1 frase corta de saludo B2B para Santiago (VP de Pagos)."}
        ],
        max_tokens=200,
        temperature=0.7
    )
    print("SUCCESS!", flush=True)
    print("Respuesta:", response.choices[0].message.content, flush=True)
except Exception as e:
    print("Error SDK:", e, flush=True)
