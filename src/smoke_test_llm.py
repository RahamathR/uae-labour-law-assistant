"""Smoke test: confirm the Groq API key works and the LLM responds."""
import os
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # loads key=value pairs from .env into environment variables

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise SystemExit("GROQ_API_KEY not found. Is .env in the repo root?")

client = Groq(api_key=api_key)

# 1. Which models can this key use?
models = sorted(m.id for m in client.models.list().data)
print("Available models:")
for model_id in models:
    print("  -", model_id)

# 2. One small test call
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
start = time.perf_counter()
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "In one sentence, what is a labour law?"},
    ],
    temperature=0,
    max_tokens=1000,
)
elapsed = time.perf_counter() - start

print(f"\nModel: {MODEL}")
print(f"Answer: {response.choices[0].message.content}")
print(f"Latency: {elapsed:.2f}s")
print(f"Tokens: {response.usage.prompt_tokens} in / {response.usage.completion_tokens} out")