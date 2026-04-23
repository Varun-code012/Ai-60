from groq import Groq
from dotenv import load_dotenv
import tiktoken, os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(messages):
    return sum(len(enc.encode(m["content"])) for m in messages)

# This Python list IS the memory — nothing more
messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant with perfect memory. "
            "Naturally reference earlier parts of the conversation when relevant."
        )
    }
]

print("Stateful chatbot — type 'quit' to exit")
print("Tip: Tell it your name in message 1, ask for it in message 5!\n")

turn = 0
while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["quit", "exit", "q"]:
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=300
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    turn += 1
    tokens = count_tokens(messages)
    print(f"AI : {reply}")
    print(f"    [Turn {turn} | Context: {tokens} tokens growing...]\n")