import chromadb

from embeddings.model import get_embedding_model


CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "resume_documents_bge"


def get_chroma_collection():
    """
    Connect to the persistent Resume Genie Chroma collection.

    The collection uses cosine distance because the BGE
    embeddings are normalized and our semantic evaluation
    is based on cosine similarity.

    Returns:
        ChromaDB collection.
    """

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=None,
        metadata={"hnsw:space": "cosine"},
    )


def store_resume_chunks(
        chunks,
        user_id: int,
        filename: str,
        ) -> int:
    """
    Generate BGE embeddings for resume chunks
    and store them in ChromaDB.

    Args:
        chunks: List of LangChain Document objects.

    Returns:
        Number of stored chunks.
    """

    embedding_model = get_embedding_model()
    collection = get_chroma_collection()

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for i, chunk in enumerate(chunks, start=1):

        chunk_id = (
            f"user_{user_id}_resume_chunk{i}"
        )

        ids.append(chunk_id)
        documents.append(chunk.page_content)

        embedding = embedding_model.encode(
            chunk.page_content,
            normalize_embeddings=True,
        )

        embeddings.append(
            embedding.tolist()
        )

        metadatas.append(
            {
                "source": filename,
                "page": chunk.metadata.get("page"),
                "page_label": chunk.metadata.get("page_label"),
                "user_id" : user_id
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks)