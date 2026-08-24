import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-0MINhr9-vEmzYLUFx-OvjQ"

endpoints = [
    ("Moonshot Kimi", "https://api.moonshot.cn/v1/models"),
    ("01.AI (Yi)", "https://api.lingyiwanwu.com/v1/models"),
    ("MiniMax", "https://api.minimax.chat/v1/models"),
    ("ModelScope", "https://api-inference.modelscope.cn/v1/models"),
    ("DeepInfra", "https://api.deepinfra.com/v1/models"),
    ("Hyperbolic", "https://api.hyperbolic.xyz/v1/models"),
    ("SambaNova", "https://api.sambanova.ai/v1/models"),
    ("OpenRouter Auth", "https://openrouter.ai/api/v1/auth/key"),
    ("ZenMux Auth", "https://zenmux.ai/api/v1/models"),
    ("AiHubMix", "https://aihubmix.com/v1/models"),
    ("SiliconFlow", "https://api.siliconflow.cn/v1/models"),
    ("Anyscale", "https://api.endpoints.anyscale.com/v1/models"),
    ("Together", "https://api.together.xyz/v1/models"),
    ("Fireworks", "https://api.fireworks.ai/inference/v1/models"),
    ("Nebius", "https://api.studio.nebius.ai/v1/models"),
    ("Novita", "https://api.novita.ai/v3/openai/models"),
    ("Bailian / DashScope", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation")
]

headers = {"Authorization": f"Bearer {key}"}

for name, url in endpoints:
    try:
        r = requests.get(url, headers=headers, timeout=3)
        print(f"[{name}] Status: {r.status_code} -> {r.text[:100]}", flush=True)
    except Exception as e:
        print(f"[{name}] Err: {e}", flush=True)
