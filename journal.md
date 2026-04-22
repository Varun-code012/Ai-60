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
Date: 22-04-2026

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

