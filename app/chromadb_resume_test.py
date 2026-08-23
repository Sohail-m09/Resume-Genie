import chromadb

from ingestion.pdf_loader import load_pdf
from processing.text_cleaner import clean_documents
from processing.text_splitter import split_documents
from embeddings.model import get_embedding_model


# ---------------------------------------------------------
# 1. Load and process the actual resume
# ---------------------------------------------------------

resume_path = r"D:\Resume-Genie\data\Sohail_Momin.pdf"

documents = load_pdf(resume_path)

cleaned_documents = clean_documents(documents)

chunks = split_documents(cleaned_documents)


print("===== RESUME PROCESSING =====")
print("Number of chunks:", len(chunks))


# ---------------------------------------------------------
# 2. Load our chosen BGE embedding model
# ---------------------------------------------------------

embedding_model = get_embedding_model()


# ---------------------------------------------------------
# 3. Create/open a dedicated Chroma collection
# ---------------------------------------------------------

client = chromadb.PersistentClient(
    path="data/chroma"
)

collection = client.get_or_create_collection(
    name="resume_documents_bge",
    embedding_function=None,
)


# ---------------------------------------------------------
# 4. Prepare chunk data
# ---------------------------------------------------------

ids = []
texts = []
embeddings = []
metadatas = []


for i, chunk in enumerate(chunks, start=1):

    chunk_id = f"resume_chunk_{i}"

    ids.append(chunk_id)
    texts.append(chunk.page_content)

    embedding = embedding_model.encode(
        chunk.page_content,
        normalize_embeddings=True,
    )

    embeddings.append(
        embedding.tolist()
    )

    metadatas.append(
        {
            "source": "Sohail_Momin.pdf",
            "page": chunk.metadata.get("page"),
            "page_label": chunk.metadata.get("page_label"),
        }
    )


# ---------------------------------------------------------
# 5. Store everything in ChromaDB
# ---------------------------------------------------------

collection.upsert(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas,
)


print("\n===== CHROMADB STORAGE =====")
print("Collection:", collection.name)
print("Stored items:", collection.count())

print("\n===== STORED RECORDS =====")

print("\n===== METADATA INSPECTION =====")

stored = collection.get(
    include=["documents", "metadatas"]
)

for i in range(len(stored["ids"])):
    print(f"\n===== RECORD {i + 1} =====")
    print("ID:", stored["ids"][i])
    print("Document:", stored["documents"][i])
    print("Metadata:", stored["metadatas"][i])