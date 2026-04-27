from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
total_tokens = 0

article = """
India's ISRO successfully launched the Aditya-L1 solar observatory.
This is India's first space-based mission to study the Sun. The spacecraft
will travel 1.5 million kilometres from Earth to the L1 Lagrange point.
Scientists expect it to study solar winds, flares, and coronal mass ejections.
This mission will improve space weather prediction and protect satellites.
"""

def llm(prompt, max_tokens=300):
    global total_tokens
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        max_tokens=max_tokens, temperature=0.5
    )
    total_tokens += resp.usage.total_tokens
    return resp.choices[0].message.content.strip()

# STEP 1: Summarize
print("STEP 1 — Summarize")
print("-"*40)
summary = llm(f"Summarize this article in exactly 2 sentences:\n\n{article}")
print(summary)

# STEP 2: Extract key claims
print("\nSTEP 2 — Extract 3 key claims")
print("-"*40)
claims = llm(f"Extract exactly 3 key factual claims as a numbered list:\n\n{summary}")
print(claims)

# STEP 3: Write tweet thread
print("\nSTEP 3 — Tweet thread")
print("-"*40)
tweets = llm(f"Write a 3-tweet thread. Each tweet under 280 chars, end with relevant emoji:\n\n{claims}", max_tokens=400)
print(tweets)

#STEP 4: Convert thread into Kannada
print("\nSTEP 4 - Kannada translation")
print("-"*40)
kannada = llm(f"Translate this thread into kannada, keeping the emojis:\n\n{tweets}", max_tokens=400)
print(kannada)

print(f"\n{'='*40}")
print(f"Total tokens across 3 steps: {total_tokens}")
print(f"Approx cost: ${total_tokens * 0.0000006:.5f}")
