from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CREATIVE = "Write one opening sentence for a thriller novel set in Ballari, India."
FACTUAL  = "What is the capital of Karnataka? Answer in one word only."

temperatures = [0.0, 0.7, 1.0, 1.5]

print("=== CREATIVE PROMPT ===")
for temp in temperatures:
    print(f"\n-- Temperature: {temp} --")
    for i in range(3):
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":CREATIVE}],
            temperature=temp,
            max_tokens=60
        )
        print(f"  Run {i+1}: {resp.choices[0].message.content.strip()}")

print("\n=== FACTUAL PROMPT ===")
for temp in [0.0, 1.5]:
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":FACTUAL}],
        temperature=temp,
        max_tokens=10
    )
    print(f"  temp={temp}: {resp.choices[0].message.content.strip()}")