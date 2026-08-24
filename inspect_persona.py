import yaml
import json

def inspect(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    print(f"=== {filepath} ===")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:1200])
    print("\n" + "="*60 + "\n")

inspect("scratch/MatrAIx-Persona-8B/persona/datasets/matraix-persona-dev-sample/persona_0001.yaml")
inspect("scratch/MatrAIx-Persona-8B/persona/datasets/matraix-persona-dev-sample/persona_0145.yaml")
