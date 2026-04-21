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