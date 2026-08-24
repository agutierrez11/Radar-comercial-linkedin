import requests

key = "sk-ai-v1-e80533e46987e996ac595537eca0adac6c4c28336ea7129e1f5c40a70ca5353c"

providers = [
    ("OpenRouter", "https://openrouter.ai/api/v1/models"),
    ("SiliconFlow", "https://api.siliconflow.cn/v1/models"),
    ("Zhipu BigModel", "https://open.bigmodel.cn/api/paas/v4/models"),
    ("Together", "https://api.together.xyz/v1/models"),
    ("DeepInfra", "https://api.deepinfra.com/v1/models"),
    ("Groq", "https://api.groq.com/openai/v1/models"),
    ("Fireworks", "https://api.fireworks.ai/inference/v1/models"),
    ("Mistral", "https://api.mistral.ai/v1/models"),
    ("Perplexity", "https://api.perplexity.ai/models"),
    ("Novita", "https://api.novita.ai/v3/openai/models"),
    ("DeepSeek", "https://api.deepseek.com/models"),
    ("AiHubMix", "https://aihubmix.com/v1/models"),
    ("OpenAI Direct", "https://api.openai.com/v1/models")
]

headers = {"Authorization": f"Bearer {key}"}

for name, url in providers:
    try:
        r = requests.get(url, headers=headers, timeout=3)
        print(f"{name}: {r.status_code} -> {r.text[:120]}")
    except Exception as e:
        print(f"{name}: Failed ({e})")
