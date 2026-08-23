import chromadb

from embeddings.model import get_embedding_model


# ---------------------------------------------------------
# 1. Connect to persistent ChromaDB
# ---------------------------------------------------------

client = chromadb.PersistentClient(
    path="data/chroma"
)


# ---------------------------------------------------------
# 2. Open our existing collection
# ---------------------------------------------------------

collection = client.get_collection(
    name="resume_documents_bge"
)


# ---------------------------------------------------------
# 3. Load the same BGE embedding model
# ---------------------------------------------------------

embedding_model = get_embedding_model()


# ---------------------------------------------------------
# 4. Create a query
# ---------------------------------------------------------

query = "What machine learning experience does this resume have?"


# ---------------------------------------------------------
# 5. Convert query into an embedding
# ---------------------------------------------------------

query_embedding = embedding_model.encode(
    query,
    normalize_embeddings=True,
).tolist()


# ---------------------------------------------------------
# 6. Search ChromaDB
# ---------------------------------------------------------

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
)


# ---------------------------------------------------------
# 7. Display results
# ---------------------------------------------------------

print("===== QUERY =====")
print(query)

print("\n===== RETRIEVED DOCUMENTS =====")

for i, document in enumerate(
    results["documents"][0],
    start=1,
):

    print(f"\n===== RESULT {i} =====")
    print("Document:", document)
    print("Metadata:", results["metadatas"][0][i - 1])
    print("Distance:", results["distances"][0][i - 1])