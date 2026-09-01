from vectorstore.chroma_store import (
    get_chroma_collection,
)


USER_ID = 13


collection = get_chroma_collection()


results = collection.get(
    where={
        "user_id": USER_ID
    }
)


print(
    "ChromaDB records for user:"
)
print(
    results["ids"]
)

print(
    "\nMetadata:"
)
print(
    results["metadatas"]
)

assert len(
    results["ids"]
) > 0

assert all(
    metadata["user_id"] == USER_ID
    for metadata in results["metadatas"]
)

print(
    "\nChromaDB user isolation verified successfully."
)