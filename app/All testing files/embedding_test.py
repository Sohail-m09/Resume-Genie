from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("BAAI/bge-small-en-v1.5")
sentences = [
    "Built REST APIs using FastAPI.",
    "Developed backend APIs for a web application.",
    "Designed graphics using Photoshop.",
]

# Now generating embeddings 
embeddings = model.encode(
    sentences,
    normalize_embeddings = True
)

print("***** Embedding INFO *****")
print("Number of sentences:", len(sentences))
print("Embedding shape:", embeddings.shape)

print("===== EMBEDDING INFORMATION =====")
print("Embedding shape:", embeddings.shape)


similarity_matrix = cosine_similarity(embeddings)

print("\n===== COSINE SIMILARITY MATRIX =====")
print(similarity_matrix)