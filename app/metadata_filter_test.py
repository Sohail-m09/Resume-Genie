import chromadb


client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_collection(
    name="resume_documents_bge"
)


print("===== ALL RESUME RECORDS =====")

all_records = collection.get(
    include=["documents", "metadatas"]
)

for i in range(len(all_records["ids"])):
    print(
        all_records["ids"][i],
        "->",
        all_records["metadatas"][i]
    )


print("\n===== FILTERED RECORDS =====")

filtered_records = collection.get(
    where={
        "source": "Sohail_Momin.pdf"
    },
    include=["documents", "metadatas"]
)

for i in range(len(filtered_records["ids"])):
    print(
        filtered_records["ids"][i],
        "->",
        filtered_records["metadatas"][i]
    )