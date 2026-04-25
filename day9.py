from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

problems = [
    "A train travels 60km/h for 2.5 hours. How far does it travel?",
    "If I have 3 boxes with 8 apples each and give away 11, how many remain?",
    "What is 15% of 840?",
    "A shirt costs Rs.450 after a 10% discount. What was the original price?",
    "If today is Wednesday, what day will it be 100 days from now?",
]

def ask(problem, cot=False):
    if cot:
        prompt = f"{problem}\nThink through this step by step, then give the final answer."
    else:
        prompt = f"{problem}\nGive only the final answer, no working."
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        max_tokens=300 if cot else 30, temperature=0
    )
    return resp.choices[0].message.content.strip(), resp.usage.total_tokens

print("="*60)
for i, prob in enumerate(problems, 1):
    print(f"\nProblem {i}: {prob}")
    direct, t1 = ask(prob, cot=False)
    cot_ans, t2 = ask(prob, cot=True)
    print(f"  Direct ({t1:3} tokens): {direct[:80]}")
    print(f"  CoT    ({t2:3} tokens):\n{cot_ans}\n")
print("="*60)


# ── HARD PROBLEMS — where CoT actually earns its cost ──

hard_problems = [
    # Multi-step logic — easy to make wrong assumptions
    "A shopkeeper buys 50 pens at Rs.2 each. He sells 30 at Rs.3.50 each and the remaining at Rs.1.50 each. What is his total profit or loss?",

    # Reverse multi-step — very easy to go wrong directly
    "After a 20% discount and then an additional 10% discount, a laptop costs Rs.36,000. What was the original price?",

    # Overlapping time — direct answers almost always wrong
    "A father is 4 times older than his son. In 20 years, he will be only twice as old. What are their current ages?",

    # Chained percentage — multiple dependent operations
    "A population grows by 10% in year 1, shrinks by 5% in year 2, then grows by 20% in year 3. If the starting population was 10,000 what is the final population?",

    # Multi-condition logic
    "There are 3 boxes. Box A has twice as many balls as Box B. Box C has 5 fewer than Box A. Together they have 55 balls. How many balls are in each box?",
]

print("\n" + "="*60)
print("HARD PROBLEMS — where CoT actually matters")
print("="*60)

direct_correct = 0
cot_correct = 0

# Known correct answers for verification
answers = ["Rs.25 profit", "Rs.50,000", "10 and 40 years", "12,474", "Box A=20, Box B=10, Box C=15"]

for i, (prob, ans) in enumerate(zip(hard_problems, answers), 1):
    print(f"\nProblem {i}: {prob[:70]}...")
    print(f"Correct answer: {ans}")

    direct, t1 = ask(prob, cot=False)
    cot_ans, t2 = ask(prob, cot=True)

    print(f"\nDirect ({t1} tokens): {direct}")
    print(f"\nCoT    ({t2} tokens):\n{cot_ans}")
    print("-"*60)