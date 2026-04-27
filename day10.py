from groq import Groq
from dotenv import load_dotenv
import json, os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

reviews = [
    "Stayed at Hotel Nakshatra for 3 nights. Rooms were clean and AC worked well. Staff very helpful. Breakfast limited. Decent for the price.",
    "Terrible experience! Room dirty, WiFi broken, front desk was rude. Complete waste of money.",
    "Amazing hotel! Beautiful decor, excellent service, food outstanding. Pricey but worth it.",
]

def extract_review(review):
    prompt = f"""Extract information from this hotel review.
Return ONLY a valid JSON object — no markdown, no code blocks, just raw JSON.

Required format:
{{
  "summary": "one sentence summary",
  "sentiment": "positive" or "negative" or "neutral",
  "rating": number 1-5,
  "pros": ["list of positives"],
  "cons": ["list of negatives"]
}}

Review: {review}

JSON:"""
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        max_tokens=300, temperature=0
    )
    raw = resp.choices[0].message.content.strip()
    try:
        return json.loads(raw), True
    except:
        cleaned = raw.replace("```json","").replace("```","").strip()
        try:
            return json.loads(cleaned), True
        except:
            return raw, False

print("Hotel Review Analyzer\n" + "="*50)
for i, review in enumerate(reviews, 1):
    print(f"\nReview {i}: {review[:55]}...")
    result, ok = extract_review(review)
    if ok:
        print(f"  Sentiment : {result['sentiment']}")
        print(f"  Rating    : {result['rating']}/5")
        print(f"  Summary   : {result['summary']}")
        print(f"  Pros      : {result['pros']}")
        print(f"  Cons      : {result['cons']}")
        print(f"  JSON OK   : ✓")
    else:
        print(f"  JSON FAILED: {result[:80]}")