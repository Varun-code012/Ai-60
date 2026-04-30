## Day 2 — Tokens & Context Windows

1. What surprised me: Kannada uses way more tokens than English (8 tokens for 5 words vs English 1 token per word).
2. What this means for my projects: If I build an app for Kannada users it will cost 5-7x more than an English app doing the same task.
3. One question I still have: Why does the same text give different token counts in different encodings?

## Day 3 — Embeddings Intuition

1. What I learned: Embeddings convert any text into a list of numbers (called a vector)
   that captures the meaning of that text. Similar meaning = similar numbers.
   The model "all-MiniLM-L6-v2" converts each sentence into 384 numbers.

2. How similarity works: Cosine similarity compares two vectors and gives a score
   between 0 and 1. High score (0.8+) = similar meaning. Low score (0.0-0.2) =
   unrelated meaning. It does not compare exact words — it compares meaning.
   "I love biryani" and "Biryani is my favorite food" score high even though
   they share no common words except biryani.

3. Why this matters for my future projects: This is the exact technology behind
   RAG (Retrieval Augmented Generation) and semantic search — which I will build
   in Week 5. When I upload a document and ask a question, embeddings are what
   find the most relevant chunks to answer from. Without understanding this Day 3
   concept, RAG would feel like magic. Now it makes sense.

## Day 4 — Your First Real API Call

1. What I built: An interactive terminal chatbot using the raw Groq API with no
   frameworks. It takes my input, sends it to Llama 3.3, and prints the response
   along with the token count used for each call.

2. Key insight: Each API call is completely stateless. The model has zero memory
   between calls — every question starts fresh. When I asked "What did I just say?"
   it had no idea. This is because we are only sending one message at a time, not
   the full conversation history. Day 7 fixes this by passing the entire message
   list with every call.

3. What I understood about the message structure: Every API call needs a list of
   messages with roles — 'system' sets the behavior, 'user' is my question, and
   'assistant' is what the model previously said. This structure is the foundation
   that every framework like LangChain is built on top of. Understanding this raw
   level makes frameworks feel transparent instead of magical.

## Day 5 — Temperature & Parameters

### What I built
Ran the same creative prompt (thriller novel set in Ballari) at 4 different
temperatures: 0.0, 0.7, 1.0, and 1.5. Also tested a factual prompt at both
extremes to observe the difference.

### Key observations
- At temp=0.0 all 3 runs gave nearly identical sentences — the model plays it safe
- At temp=1.5 all 3 runs were completely different — sometimes creative, sometimes weird
- The factual question (capital of Karnataka) answered "Bengaluru" correctly at
  ALL temperatures — temperature barely affects factual answers
- Sweet spot for creative writing felt like 0.7 — varied but still coherent

### My temperature rule of thumb
- 0.0 – 0.3 → facts, code, data extraction (need consistency)
- 0.7 – 1.0 → creative writing, personas, storytelling (need variety)
- 1.0 – 1.2 → brainstorming, idea generation (need diversity)
- Above 1.5 → almost never useful, output gets incoherent

### What surprised me
Temperature has almost zero effect on factual answers — the model's training
is strong enough to override randomness when the answer is clear-cut.
For creative tasks though, even 0.3 difference in temperature noticeably
changes the output style.

### One question I still have
What exactly is top_p (nucleus sampling) and how is it different from
temperature? Should I ever tune both at the same time?

## Day 6 Challenge — Coding-Only Bot
- Learned that vague system prompts fail — specificity is everything
- Explicit allow-list + deny-list works much better than a single rule
- Giving the model exact refusal wording makes responses consistent
- "Even if user insists" line prevents simple jailbreak attempts

## Day 7 — Stateful Chatbot with Memory

### What I built
A CLI chatbot that remembers the entire conversation by passing the full
message history as a Python list with every API call. Added a token counter
using tiktoken to watch context grow in real time.

### How memory actually works at the API level
The OpenAI/Groq API is completely stateless — it remembers nothing between
calls. WE simulate memory by maintaining a messages list in Python and
sending the entire conversation history with every single API call.
Memory = a growing Python list. Nothing more, nothing less.

### What I observed
- Told the bot my name and favorite food in message 1
- Asked for them in message 5 — it remembered correctly
- Token count grew from ~50 tokens at turn 1 to ~500+ by turn 5
- Every single turn adds both the user message AND assistant reply to context
- The more you chat, the more tokens you consume per call

### What happens at 500 turns?
The context keeps growing linearly. Eventually it hits the 128K token limit
and the API throws a context_length_exceeded error. The entire conversation
breaks. This is why production chatbots need smarter memory strategies.

### The three production solutions (to build in Week 3)
1. Truncation — drop oldest messages when context gets too long
2. ConversationBufferWindowMemory — keep only last N turns (LangChain)
3. ConversationSummaryMemory — summarize old turns instead of deleting
   (best quality, slightly more expensive)

### Biggest insight of Week 1
LangChain's memory abstractions are just automated versions of the
messages list I built manually today. Now that I've built it from scratch,
frameworks make complete sense — they're not magic, just convenience.

### Week 1 complete — what I can now do
- Make raw API calls with full parameter control
- Count tokens and estimate costs before calling the API
- Compute semantic similarity between sentences using embeddings
- Build an interactive API loop from scratch
- Control model behavior with temperature
- Create distinct AI personas using only system prompts
- Build a stateful chatbot with manual memory management

### One question I still have
How does ConversationSummaryMemory decide what to summarize and what to
keep? Does it summarize after every turn or only when context gets too long?


## Day 8 — Zero-shot vs Few-shot Prompting
Date: 24-04-2026

### What I built
A headline classifier that tests 3 prompting approaches — zero-shot,
one-shot, and five-shot — on the same set of news headlines.
Compared accuracy and output consistency across all three approaches.

### What zero-shot, one-shot, five-shot mean
- Zero-shot : no examples given — just ask the model directly
- One-shot  : one example shown before the question
- Five-shot : five examples shown before the question
The more examples you give, the more guided the model's answer becomes.

### Problem I faced and how I fixed it
Model was returning extra text like "Category: Sports" and
"Headline: ..." instead of just the single word.

Fix 1 — moved instructions to system prompt instead of user prompt.
         Model treats system instructions more strictly.
Fix 2 — set max_tokens=5 so the model physically cannot output
         a full sentence. Forces a single word response.

### Accuracy test results

Easy headlines (5 total):
- Zero-shot  : 5/5 — 100%
- One-shot   : 5/5 — 100%
- Five-shot  : 5/5 — 100%
- Conclusion : all 3 tied on easy headlines — no difference

Ambiguous headlines (10 total):
- Zero-shot  : 7/10
- One-shot   : 7/10
- Five-shot  : 7/10
- Winner     : All approaches tied — prompts are strong!
Conclusion: use Zero-shot in production (same accuracy, lower cost).

### Headlines that confused the model
- (write which ambiguous headlines got wrong answers and why)

### Key insights from today

1. For clear headlines — zero-shot is enough. No need for examples.
   Use zero-shot in production for obvious categories.

2. For ambiguous headlines — few-shot examples genuinely help.
   Examples guide the model when the category boundary is unclear.

3. Few-shot costs more tokens on EVERY call — not just once.
   If you make 1000 API calls per day, five-shot costs 5x more
   than zero-shot across all those calls. Always ask: is the
   accuracy improvement worth the cost increase?

4. max_tokens is a powerful format control tool — not just a cost
   tool. Setting it to 5 forced single-word output better than
   any prompt instruction alone.

5. System prompt vs user prompt — system prompt instructions are
   followed more strictly. Always put format requirements in the
   system prompt.

### My rule for choosing shot type in real apps
- Category is obvious (Sports, Tech, Finance) → Zero-shot
- Category is ambiguous or overlapping → Few-shot (3-5 examples)
- Output format must be strict → System prompt + low max_tokens

### Token cost comparison (approximate)
- Zero-shot  : ~20 tokens per call
- One-shot   : ~50 tokens per call
- Five-shot  : ~120 tokens per call
At 1000 calls/day: Zero-shot = $0.012 vs Five-shot = $0.072

### One question I still have
At what point does adding more examples (10-shot, 20-shot) stop
improving accuracy? Is there a point of diminishing returns?


## Day 9 — Chain-of-Thought Prompting
Date: 24-04-2026

### What I observed on simple problems
Llama 3.3 70B is powerful enough to solve all 5 simple problems
correctly even without CoT. Direct and CoT tied 5/5.

### Why CoT still matters — the real conditions
CoT makes a genuine difference when ALL of these are true:
1. Problem requires 3+ dependent calculation steps
2. An error in step 1 ruins all following steps
3. The model being used is smaller or weaker
4. The stakes of a wrong answer are high

### Hard problem results
- Simple problems  : Direct = CoT (Llama 3.3 is strong)
- Hard problems    : CoT wins — father-son, three-boxes failed direct
- Reverse discount : CoT wins — chained percentages trip direct answers

### My real-world rule
- Using GPT-4o / Llama 3.3 70B + simple problems → skip CoT, save tokens
- Using smaller models (Llama 3.2 1B, Gemma 2B) → CoT helps a lot
- Any problem with 3+ chained steps → always use CoT regardless of model
- Production apps → test both, measure accuracy difference, then decide

### Cost vs accuracy tradeoff
CoT costs 5-7x more tokens. On 1000 calls/day that's a real cost.
Never use CoT by default — only when accuracy testing proves it helps.

## Day 10 — Output Format Control
- Magic phrase: "ONLY valid JSON, no markdown, no explanation"
- temperature=0 is critical for format consistency
- Always add json.loads() fallback with .replace() cleanup
- This skill is used in every real AI app — extractors, classifiers, summarizers

## Day 11 — Prompt Chaining
- Each prompt output becomes the next prompt input — simple but powerful
- This is exactly what LangChain automates — now I understand why it exists
- 3-step chain total: ~450 tokens vs ~150 for single prompt
- When to chain: when one prompt cannot reliably do the full task alone

## Day 12 — Project 1: AI Text Analyzer (Core Build)

### What I built
A command-line text analyzer tool in project1/analyzer.py that takes
any text via --text or --file flag, sends it to Llama 3.3 via Groq API,
parses the structured JSON response, and displays formatted results.

### How it works (architecture)
User input (--text or --file)
    ↓
analyzer.py reads the text
    ↓
Prompt asks LLM to return JSON with summary, sentiment, keywords
    ↓
json.loads() parses the response
    ↓
display() formats and prints the results to terminal

### Problem I faced and how I fixed it
Problem : load_dotenv() couldn't find .env because project1 is a
          subfolder — it was looking in the wrong directory.

Fix     : Used pathlib to explicitly point to parent folder's .env:
          load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

Lesson  : Always use Path(__file__) for relative paths in subfolders.
          Never assume the current working directory is correct.

### Second problem — imports in wrong place
Problem : Placed "from pathlib import Path" in the middle of the file
          instead of at the top with other imports.

Fix     : Moved all imports to the top of the file.

Lesson  : Python imports always go at the very top of the file.
          Order matters: imports → load_dotenv → client → functions → main

### What I observed
- Short text (7 words) only returns 3 keywords — model can only find
  what's genuinely there. Cannot invent 5 keywords from 7 words.
- Longer text gives all 5 keywords as expected.
- temperature=0 gives consistent JSON structure every time.
- json.loads() validation is essential — always add the fallback cleanup.

### Key code pattern I learned today
argparse lets you build clean CLI tools with named flags:
  --text  for direct string input
  --file  for reading from a file
  --output for saving results (Day 13)
This pattern is used in almost every professional CLI tool.

### Test results
Tested on 3 texts:
1. ISRO solar mission (positive, Tech) ✓
2. Worst movie ever (negative, Entertainment) ✓  
3. Short text — 7 words (only 3 keywords returned — expected) ✓

### What this project does that's actually useful
Takes unstructured text → returns structured data in seconds.
Real use case: analyzing 100s of hotel reviews automatically,
classifying news articles, monitoring social media sentiment.
This is the core pattern behind most NLP products.

### One question I still have
How do I handle the case where the model returns valid JSON but
with wrong keys — for example "keyword" instead of "keywords"?
Should I validate the keys after parsing?


## Day 13 — Project 1 Extended

### What I added today
1. Topic categorization — 8 categories: Tech, Sports, Finance,
   Health, Education, Entertainment, Politics, General
2. --output flag — saves results to .txt file with timestamp
3. Error handling — friendly messages for short text, missing
   files, and API failures
4. --help flag — clear usage instructions with examples

### All flags working
--text   : direct text input         ✓
--file   : read from .txt file       ✓
--output : save results to file      ✓
--help   : shows usage clearly       ✓

### Edge cases handled
Short text (Hi)     : "Text too short" error    ✓
File not found      : "File not found" error     ✓
API failure         : "Check API key" message    ✓

### Key code patterns learned today
1. argparse epilog — adds examples section to --help output
2. datetime.now().strftime() — formats timestamp in output file
3. try/except ValueError — catches custom validation errors
4. try/except FileNotFoundError — handles missing file gracefully
5. Nested try/except — different error types need different messages

### What results.txt looks like
==================================================
AI TEXT ANALYZER RESULTS
Generated : 2026-04-30 11:25
==================================================
Words     : 6
Topic     : Sports
Sentiment : POSITIVE (score: 0.9)
Summary   : India won the cricket final against Australia
Keywords  : India, Australia, cricket, final
==================================================

### Project 1 is now a real usable tool
Anyone can clone this repo, install dependencies, and use it
immediately. That is what makes it portfolio-worthy — not just
a script, but a complete CLI tool with proper UX.

### Biggest lesson of Day 13
Error handling is what separates a script from a real tool.
A script crashes on bad input. A real tool explains what went
wrong and how to fix it. Always handle errors before shipping.

### One question I still have
Can I add a --batch flag that reads multiple texts from a CSV
file and analyzes all of them at once? That would make this
tool much more powerful for real use cases.



