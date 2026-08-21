import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

sentences = [
    "Built REST APIs using FastAPI.",
    "Developed backend APIs for a web application.",
]

embeddings = model.encode(
    sentences,
    normalize_embeddings = True,
)

vector_a = embeddings[0]
vector_b = embeddings[1]

similarity = cosine_similarity(
    [vector_a],
    [vector_b],
)[0][0]

manual_similarity = np.dot(vector_a, vector_b)

print("Cosine similarity using sklearn:", similarity)
print("Cosine similarity manually:", manual_similarity)