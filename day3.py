from sentence_transformers import SentenceTransformer
import numpy as np

# Downloads once (~80MB), cached locally — free forever
model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "I love eating biryani",
    "Biryani is my favorite food",
    "The stock market crashed today",
    "Dogs make wonderful pets",
    "I enjoy spicy Indian cuisine",
]

embeddings = model.encode(sentences)

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("Cosine similarity scores:")
for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        sim = cosine_sim(embeddings[i], embeddings[j])
        s1 = sentences[i][:28].ljust(28)
        s2 = sentences[j][:28].ljust(28)
        print(f"  {s1} vs {s2} -> {sim:.3f}")