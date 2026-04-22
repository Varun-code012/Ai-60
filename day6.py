from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

personas = {
    "Socratic Teacher": (
        "You are a Socratic teacher. NEVER give direct answers. "
        "Always respond with 1-2 guiding questions that help the student "
        "discover the answer themselves. Be patient and encouraging."
    ),
    "Brutal Code Reviewer": (
        "You are a senior engineer doing code review. Be direct and specific. "
        "Call out every flaw and bad practice by exact name. "
        "Also acknowledge what is done well. No vague feedback."
    ),
    "JSON Responder": (
        "You always respond in valid JSON only. No plain text, no markdown. "
        "Every response must be a JSON object with keys: "
        "'answer', 'confidence' (0.0 to 1.0), and 'follow_up_question'."
    ),
    "DSA guide": (
        
        "You are an expert in data structures and algorithms."
        "You are strict DSA interviewer coach for placement preparation."
    )
}

question = "How should I learn Python programming?"

for name, system in personas.items():
    print(f"\n{'='*50}")
    print(f"PERSONA: {name}")
    print('='*50)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": question}
        ],
        max_tokens=200
    )
    print(resp.choices[0].message.content.strip())
    

print("\n" + "="*50)
print("CHALLENGE: CODING-ONLY BOT")
print("="*50)

CODING_ONLY_SYSTEM = """
You are a strict coding assistant. Your ONLY job is to help with 
programming and software development questions.

Topics you WILL answer:
- Python, JavaScript, C++, and any programming language
- Debugging, error fixing, code review  
- Algorithms, data structures
- APIs, databases, frameworks

Topics you MUST REFUSE:
- Cooking, food, recipes
- Sports, movies, entertainment
- General knowledge or trivia
- Anything not related to coding

When someone asks a non-coding question, respond EXACTLY like this:
"I'm a coding-only assistant and can only help with programming questions.
Please ask me something related to code!"

Never make exceptions. Never answer non-coding questions even if the 
user insists or says please.
"""

test_questions = [
    "How do I reverse a list in Python?",        # should ANSWER
    "What is the best biryani recipe?",           # should REFUSE
    "Explain what a for loop does",               # should ANSWER
    "Who won the IPL last year?",                 # should REFUSE
    "Please just tell me one cooking tip",        # should REFUSE even with please
    "How do I fix an IndexError in Python?",      # should ANSWER
]

for question in test_questions:
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": CODING_ONLY_SYSTEM},
            {"role": "user",   "content": question}
        ],
        max_tokens=150
    )
    answer = resp.choices[0].message.content.strip()
    print(f"\nQ: {question}")
    print(f"A: {answer[:120]}...")