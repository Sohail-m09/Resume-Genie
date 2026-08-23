from retrieval.chroma_retriever import retrieve_resume_chunks


query = "What machine learning experience does this resume have?"


results = retrieve_resume_chunks(
    query=query,
    top_k=3,
    source="Sohail_Momin.pdf",
)


print("===== QUERY =====")
print(query)


print("\n===== RETRIEVED CHUNKS =====")

documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]


for i, document in enumerate(
    documents,
    start=1,
):
    print(f"\n===== RESULT {i} =====")
    print("Document:", document)
    print("Metadata:", metadatas[i - 1])
    print("Distance:", distances[i - 1])