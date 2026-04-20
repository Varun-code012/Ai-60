import tiktoken

def analyze_tokens(text, label):
    enc = tiktoken.get_encoding("o200k_base")
    tokens = enc.encode(text)
    wc = len(text.split())
    tc = len(tokens)
    print(f"--- {label} ---")
    print(f"Words: {wc} | Tokens: {tc} | Ratio: {tc/wc:.2f}")
    print()

analyze_tokens("The quick brown fox jumps over the lazy dog.", "English")
analyze_tokens("ನಾನು ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡುತ್ತೇನೆ.", "Kannada")
analyze_tokens("def fibonacci(n): return n if n<=1 else fibonacci(n-1)+fibonacci(n-2)", "Code")

def estimate_cost(prompt, response_tokens=200):
    enc = tiktoken.get_encoding("o200k_base")
    input_tokens = len(enc.encode(prompt))
    
    # GPT-4o-mini pricing used as reference benchmark
    input_cost  = (input_tokens / 1_000_000) * 0.15
    output_cost = (response_tokens / 1_000_000) * 0.60
    total = input_cost + output_cost
    
    print(f"--- Cost Estimate ---")
    print(f"Input tokens   : {input_tokens}")
    print(f"Output tokens  : {response_tokens} (estimated)")
    print(f"Total cost     : ${total:.6f}")
    print(f"Calls for $1   : {int(1/total):,}")
    print()

print("=== COST ESTIMATOR ===")
estimate_cost("Summarize the Indian independence movement in 3 bullet points.")
estimate_cost("ಕನ್ನಡ ಸಾಹಿತ್ಯದ ಇತಿಹಾಸವನ್ನು ವಿವರಿಸಿ.")