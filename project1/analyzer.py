from groq import Groq
from dotenv import load_dotenv
import argparse, json, os
from datetime import datetime

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TOPICS = ["Tech","Sports","Finance","Health","Education","Entertainment","Politics","General"]

def analyze_text(text):
    if len(text.strip()) < 10:
        raise ValueError("Text too short — please provide at least 10 characters.")
    prompt = f"""Analyze this text. Return ONLY raw JSON, no markdown.

{{
  "summary": "1-2 sentence summary",
  "sentiment": "positive" or "negative" or "neutral",
  "sentiment_score": number 0.0 to 1.0,
  "keywords": ["kw1","kw2","kw3","kw4","kw5"],
  "topic": one of {TOPICS},
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

def format_output(data, text):
    lines = [
        "="*50,
        "AI TEXT ANALYZER RESULTS",
        f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "="*50,
        f"Words     : {data.get('word_count', len(text.split()))}",
        f"Topic     : {data.get('topic','General')}",
        f"Sentiment : {data['sentiment'].upper()} (score: {data['sentiment_score']})",
        f"Summary   : {data['summary']}",
        f"Keywords  : {', '.join(data['keywords'])}",
        "="*50,
    ]
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="AI Text Analyzer — analyzes any text using LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python analyzer.py --text 'Your text here'\n  python analyzer.py --file article.txt --output results.txt"
    )
    parser.add_argument("--text",   type=str, help="Text string to analyze")
    parser.add_argument("--file",   type=str, help="Path to .txt file to analyze")
    parser.add_argument("--output", type=str, help="Save results to this file path")
    args = parser.parse_args()

    try:
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
        output = format_output(result, text)
        print(output)

        if args.output:
            with open(args.output,"w") as f:
                f.write(output)
            print(f"\nSaved to: {args.output}")

    except ValueError as e:
        print(f"Input error: {e}")
    except FileNotFoundError:
        print(f"File not found: {args.file}")
    except Exception as e:
        print(f"Error: {e}\nCheck your API key and internet connection.")

if __name__ == "__main__":
    main()