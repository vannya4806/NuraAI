import os
import requests

api_key = os.environ.get("GROQ_API_KEY")
print("API key kebaca?", "YA" if api_key else "TIDAK ADA")
if api_key:
    print("Awalan key:", api_key[:8] + "...")

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "openai/gpt-oss-120b",
        "max_tokens": 50,
        "messages": [{"role": "user", "content": "Halo, siapa kamu?"}],
    },
    timeout=15,
)

print("Status code:", response.status_code)
print("Response body:", response.text)