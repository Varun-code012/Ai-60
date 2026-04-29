from groq import Groq
from dotenv import load_dotenv
import argparse, json, os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_text(text):
    prompt = f"""Analyze the following text. Return ONLY a valid JSON object.
No markdown, no code blocks, just raw JSON.

{{
  "summary": "1-2 sentence summary",
  "sentiment": "positive" or "negative" or "neutral",
  "sentiment_score": number from 0.0 to 1.0,
  "keywords": ["kw1", "kw2", "kw3", "kw4", "kw5"],
  "word_count": number
}}

Text: {text}

JSON:"""
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}],
        max_tokens=400, temperature=0
    )
    raw = resp.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except:
        cleaned = raw.replace("```json","").replace("```","").strip()
        return json.loads(cleaned)

def display(data):
    print("\n" + "="*50)
    print("AI TEXT ANALYZER")
    print("="*50)
    print(f"Words      : {data.get('word_count','?')}")
    print(f"Sentiment  : {data['sentiment'].upper()} (score: {data['sentiment_score']})")
    print(f"Summary    : {data['summary']}")
    print(f"Keywords   : {', '.join(data['keywords'])}")
    print("="*50)

def main():
    parser = argparse.ArgumentParser(description="AI Text Analyzer")
    parser.add_argument("--text", type=str, help="Text to analyze")
    parser.add_argument("--file", type=str, help="Path to .txt file")
    args = parser.parse_args()

    if args.file:
        with open(args.file,"r") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Enter text (blank line to finish):")
        lines=[]
        while True:
            line=input()
            if line=="": break
            lines.append(line)
        text=" ".join(lines)

    print("Analyzing...")
    result = analyze_text(text)
    display(result)

if __name__ == "__main__":
    main()