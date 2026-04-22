from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(question, system="You are a helpful assistant."):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": question}
        ],
        max_tokens=300,
        temperature=0.7
    )
    answer = response.choices[0].message.content
    tokens = response.usage.total_tokens
    return answer, tokens

print("Ask anything. Type quit to exit.")
while True:
    q = input("You: ").strip()
    if q.lower() in ["quit","exit","q"]:
        break
    answer, tokens = ask_llm(q)
    print(f"AI : {answer}")
    print(f"    [tokens used: {tokens}]")