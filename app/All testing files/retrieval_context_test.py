from retrieval.chroma_retriever import retrieve_resume_context


query = "What machine learning experience does this resume have?"

context = retrieve_resume_context(
    query=query,
    top_k=3,
)


print("===== RETRIEVED CONTEXT =====")

for i, item in enumerate(context, start=1):

    print(f"\n===== CHUNK {i} =====")

    print("Text:")
    print(item["text"])

    print("\nMetadata:")
    print(item["metadata"])

    print("\nDistance:")
    print(item["distance"])