from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


sentences = [
    "Payment must be completed within 30 days.",
    "The invoice should be paid within one month.",
    "The weather is sunny today."
]


embeddings = model.encode(sentences)


print("Number of embeddings:", len(embeddings))

print("Size of each embedding:", len(embeddings[0]))