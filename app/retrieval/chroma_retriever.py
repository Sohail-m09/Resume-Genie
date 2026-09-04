import chromadb
from embeddings.model import get_embedding_model

CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "resume_documents_bge"


def get_resume_collection():
    """
    Connect to the persistent ChromaDB collection
    containing resume embeddings.

    Returns:
        ChromaDB collection.
    """

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    return client.get_collection(
        name=COLLECTION_NAME
    )


def retrieve_resume_chunks(
    query: str,
    top_k: int = 3,
    source: str | None = None,
    user_id: int | None = None,
    resume_id: int | None = None,
) -> dict:
    """
    Retrieve the most relevant resume chunks for a query.

    Args:
        query: User/search query.
        top_k: Number of chunks to retrieve.
        source: Optional source filename filter.
        user_id: Optional user ID for multi-user isolation.
        resume_id: Optional specific resume ID filter.

    Returns:
        ChromaDB retrieval result.
    """

    embedding_model = get_embedding_model()

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    collection = get_resume_collection()

    query_kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
    }

    filters = []

    if user_id is not None:
        filters.append(
            {
                "user_id": user_id
            }
        )

    if resume_id is not None:
        filters.append(
            {
                "resume_id": resume_id
            }
        )

    if source:
        filters.append(
            {
                "source": source
            }
        )

    if len(filters) == 1:
        query_kwargs["where"] = filters[0]

    elif len(filters) > 1:
        query_kwargs["where"] = {
            "$and": filters
        }

    results = collection.query(
        **query_kwargs
    )

    return results


def retrieve_resume_context(
    query: str,
    top_k: int = 3,
    source: str | None = None,
    user_id: int | None = None,
    resume_id: int | None = None,
) -> list[dict]:
    """
    Retrieve relevant resume chunks in an application-friendly format.

    Args:
        query: User query.
        top_k: Number of chunks to retrieve.
        source: Optional source filter.
        user_id: Optional user ID for multi-user isolation.
        resume_id: Optional resume ID filter.

    Returns:
        List of retrieved chunks with text, metadata, and distance.
    """

    results = retrieve_resume_chunks(
        query=query,
        top_k=top_k,
        source=source,
        user_id=user_id,
        resume_id=resume_id,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context = []

    for i, document in enumerate(documents):
        context.append(
            {
                "text": document,
                "metadata": metadatas[i],
                "distance": distances[i],
            }
        )

    return context