from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

headlines = [
    "India wins cricket World Cup in thrilling final",
    "Google releases new AI model beating GPT-4",
    "Stock market crashes amid inflation fears",
    "New study links coffee to longer life",
    "Mumbai rains cause massive traffic disruption",
]

def classify(headline, system_prompt):
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": headline}
        ],
        max_tokens=5,
        temperature=0
    )
    return resp.choices[0].message.content.strip()

# Zero-shot system prompt
ZERO = (
    "You classify news headlines. "
    "Reply with ONLY one word from: Tech, Sports, Finance, Health, General. "
    "No other words. No punctuation. Just the single category word."
)

# One-shot system prompt
ONE = (
    "You classify news headlines. "
    "Reply with ONLY one word from: Tech, Sports, Finance, Health, General. "
    "No other words. No punctuation. Just the single category word.\n\n"
    "Example:\n"
    "Input: Virat Kohli scores century in test match\n"
    "Output: Sports"
)

# Five-shot system prompt
FIVE = (
    "You classify news headlines. "
    "Reply with ONLY one word from: Tech, Sports, Finance, Health, General. "
    "No other words. No punctuation. Just the single category word.\n\n"
    "Examples:\n"
    "Input: Virat Kohli scores century in test match\nOutput: Sports\n"
    "Input: Apple launches new MacBook with M4 chip\nOutput: Tech\n"
    "Input: Sensex drops 1000 points in single session\nOutput: Finance\n"
    "Input: Daily walking reduces heart disease risk\nOutput: Health\n"
    "Input: Mumbai trains resume after floods\nOutput: General"
)

print(f"\n{'Headline':<48} {'Zero':>8} {'One':>8} {'Five':>8}")
print("-" * 80)
for h in headlines:
    z = classify(h, ZERO)
    o = classify(h, ONE)
    f = classify(h, FIVE)
    print(f"{h[:47]:<48} {z:>8} {o:>8} {f:>8}")
    
    
# ── INDIVIDUAL TESTING SECTION ──────────────────────────

test_headlines = [
    "Ballari students win national robotics championship",  # Tech or General?
    "RBI raises interest rates by 25 basis points",        # Finance
    "Rohit Sharma retires from Test cricket",              # Sports
    "New vaccine reduces malaria deaths by 70%",           # Health
    "Karnataka government launches free laptop scheme",    # General or Tech?
]

correct_answers = ["Tech", "Finance", "Sports", "Health", "General"]

def score_shot(shot_name, system_prompt):
    print(f"\n{'='*50}")
    print(f"TESTING: {shot_name}")
    print(f"{'='*50}")
    print(f"{'Headline':<45} {'Got':>8} {'Expected':>10} {'✓/✗':>5}")
    print("-" * 72)

    correct = 0
    for headline, expected in zip(test_headlines, correct_answers):
        result = classify(headline, system_prompt)
        match = "✓" if result.lower() == expected.lower() else "✗"
        if match == "✓":
            correct += 1
        print(f"{headline[:44]:<45} {result:>8} {expected:>10} {match:>5}")

    print(f"\nScore: {correct}/{len(test_headlines)}")
    print(f"Accuracy: {(correct/len(test_headlines))*100:.0f}%")

# Test each shot type one by one
score_shot("ZERO-SHOT", ZERO)
score_shot("ONE-SHOT",  ONE)
score_shot("FIVE-SHOT", FIVE)

# Final comparison summary
print(f"\n{'='*50}")
print("SUMMARY")
print(f"{'='*50}")
print("Zero-shot : fastest, cheapest, no examples needed")
print("One-shot  : one example, small cost increase")
print("Five-shot : most guided, highest token cost")
print("\nCheck scores above to see which performed best on your data.")


# ── ACCURACY TEST WITH AMBIGUOUS HEADLINES ──────────────

ambiguous_headlines = [
    # Ambiguous — could be Tech OR General
    "Ballari students win national robotics championship",
    # Ambiguous — could be Health OR General  
    "Karnataka government launches free hospital scheme",
    # Ambiguous — could be Finance OR General
    "Petrol prices rise again in major Indian cities",
    # Ambiguous — could be Tech OR Finance
    "Bitcoin hits new all-time high as investors rush in",
    # Ambiguous — could be Sports OR General
    "India to host 2036 Olympics says government official",
    # Ambiguous — could be Health OR Tech
    "AI detects cancer faster than doctors in new study",
    # Ambiguous — could be General OR Politics
    "Karnataka CM announces new scheme for farmers",
    # Ambiguous — could be Tech OR Education
    "IIT Bombay launches free online AI course for students",
    # Ambiguous — could be Finance OR General
    "Gold prices touch record high ahead of Diwali season",
    # Ambiguous — could be Sports OR Finance
    "IPL franchise sold for record Rs.10,000 crore",
]

# These are YOUR expected answers — you decide what's correct
# This is intentional — ambiguous headlines have no single right answer
your_expected = [
    "Tech",     # robotics = Tech
    "General",  # government scheme = General
    "Finance",  # prices = Finance
    "Finance",  # Bitcoin = Finance
    "Sports",   # Olympics = Sports
    "Tech",     # AI study = Tech
    "General",  # government announcement = General
    "Education", # — wait, Education isn't even in our list!
    "Finance",  # gold prices = Finance
    "Sports",   # IPL = Sports
]

# Notice: "Education" isn't in our category list — 
# this tests what the model does with edge cases

def score_shot(shot_name, system_prompt):
    print(f"\n{'='*55}")
    print(f"TESTING: {shot_name}")
    print(f"{'='*55}")
    print(f"{'Headline':<42} {'Got':>9} {'Expected':>9} {'✓/✗':>4}")
    print("-" * 68)

    correct = 0
    wrong_ones = []

    for headline, expected in zip(ambiguous_headlines, your_expected):
        result = classify(headline, system_prompt)
        match = "✓" if result.lower() == expected.lower() else "✗"
        if match == "✓":
            correct += 1
        else:
            wrong_ones.append((headline, result, expected))
        print(f"{headline[:41]:<42} {result:>9} {expected:>9} {match:>4}")

    accuracy = (correct / len(ambiguous_headlines)) * 100
    print(f"\nScore    : {correct}/{len(ambiguous_headlines)}")
    print(f"Accuracy : {accuracy:.0f}%")

    if wrong_ones:
        print(f"\nWrong predictions:")
        for h, got, exp in wrong_ones:
            print(f"  '{h[:45]}' → got '{got}', expected '{exp}'")

    return accuracy

# Run all 3 and compare
z_score = score_shot("ZERO-SHOT", ZERO)
o_score = score_shot("ONE-SHOT",  ONE)
f_score = score_shot("FIVE-SHOT", FIVE)

# Final comparison
print(f"\n{'='*55}")
print("FINAL ACCURACY COMPARISON")
print(f"{'='*55}")
print(f"Zero-shot : {z_score:.0f}%")
print(f"One-shot  : {o_score:.0f}%")
print(f"Five-shot : {f_score:.0f}%")

if f_score > z_score:
    diff = f_score - z_score
    print(f"\nFive-shot beats Zero-shot by {diff:.0f}%")
    print("Extra token cost may be justified for ambiguous data.")
elif z_score == f_score:
    print("\nAll approaches tied — your prompts are strong!")
    print("Conclusion: use Zero-shot in production (same accuracy, lower cost).")
else:
    print("\nZero-shot actually won — examples confused the model here.")