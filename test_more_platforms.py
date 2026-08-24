import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

key = "sk-0MINhr9-vEmzYLUFx-OvjQ"

endpoints = [
    ("Gitee AI", "https://ai.gitee.com/v1/chat/completions", "Qwen2.5-72B-Instruct"),
    ("StepFun", "https://api.stepfun.com/v1/chat/completions", "step-1-8k"),
    ("Baichuan", "https://api.baichuan-ai.com/v1/chat/completions", "Baichuan2-Turbo"),
    ("Zhipu AI Direct", "https://open.bigmodel.cn/api/paas/v4/chat/completions", "glm-4"),
    ("InternLM (Sensetime)", "https://internlm-chat.intern-ai.org.cn/puyu/api/v1/chat/completions", "internlm2.5-latest"),
    ("Infinigence (Infini-AI)", "https://cloud.infini-ai.com/maas/v1/chat/completions", "qwen2.5-72b-instruct"),
    ("Baidu Qianfan", "https://qianfan.baidubce.com/v2/chat/completions", "ERNIE-Speed-8K"),
    ("Tencent Hunyuan", "https://api.hunyuan.tencent.com/v1/chat/completions", "hunyuan-lite"),
    ("Alibaba Cloud Bailian Compatible", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen-max"),
    ("Alibaba Cloud Intl", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen-max"),
]

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

payload = {
    "messages": [{"role": "user", "content": "Di 'OK'"}],
    "max_tokens": 10
}

for name, url, mod in endpoints:
    payload["model"] = mod
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=4)
        print(f"[{name}] Status: {r.status_code} -> {r.text[:120]}", flush=True)
    except Exception as e:
        print(f"[{name}] Err: {e}", flush=True)
