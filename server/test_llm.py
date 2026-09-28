from dotenv import load_dotenv
import os

from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(api_key=os.getenv("HF_TOKEN"))

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    messages=[
        {
            "role": "user",
            "content": "Explain what this function does: def add(a, b): return a + b",
        }
    ],
    max_tokens=200,
    temperature=0.1,
)

print(response.choices[0].message.content)
