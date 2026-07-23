from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import anthropic

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NormalizeRequest(BaseModel):
    strings: list[str]

@app.post("/api/normalize")
async def normalize_data(req: NormalizeRequest):
    if not req.strings:
        return {}

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Missing API Key")
        return {}

    client = anthropic.Anthropic(api_key=api_key)

    prompt = """Eres un experto en normalización de datos geográficos para un CRM B2B.
Analiza la siguiente lista de strings que tienen el formato: 'Empresa | Posición'.
Tu objetivo es inferir el País (y Ciudad si es posible) más probable de esa persona.

REGLAS:
1. Si el texto menciona una ubicación explícitamente, extrae esa ciudad y el país correspondiente.
2. Si es una empresa que opera casi exclusivamente en un país (ej. Clip, Konfío), asume la sede principal.
3. Si no hay indicios geográficos, pon "Desconocido".
4. Los países deben estar en español.

RESPONDE ESTRICTAMENTE CON UN ARRAY JSON VÁLIDO. SIN TEXTO ANTES NI DESPUÉS.
Formato esperado:
[
  { "input": "Kанкун, ROO | Director", "country": "México", "city": "Cancún" },
  { "input": "Clip | Data Scientist", "country": "México", "city": "CDMX" }
]

Strings a analizar:\n"""
    
    for s in req.strings:
        prompt += f"- {s}\n"
        
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            temperature=0.0,
            system="Responde estricta y únicamente con un Array JSON válido. No uses markdown.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.content[0].text
        start_idx = content.find("[")
        end_idx = content.rfind("]")
        if start_idx != -1 and end_idx != -1:
            results = json.loads(content[start_idx:end_idx+1])
            final_dict = {}
            for r in results:
                final_dict[r.get("input", "")] = {
                    "country": r.get("country", "Desconocido"),
                    "city": r.get("city", "Desconocido")
                }
            return final_dict
        return {}
    except Exception as e:
        print("Error con Claude:", e)
        return {}
