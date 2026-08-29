import chromadb


client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_or_create_collection(
    name="resume_documents"
)


collection.add(
    ids=["resume_chunk_001"],
    documents=[
        "Built several machine learning projects using scikit-learn and XGBoost."
    ],
    metadatas=[
        {
            "source": "Sohail_Momin.pdf",
            "page": 1,
        }
    ],
)


print("===== CHROMADB TEST =====")
print("Collection name:", collection.name)
print("Number of stored items:", collection.count())