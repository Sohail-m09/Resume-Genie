from sentence_transformers import SentenceTransformer
from functools import lru_cache

MODEL_NAME = "BAAI/bge-small-en-v1.5"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """
    Load the BGE embedding model once and reuse it.

    Returns:
        Cached SentenceTransformer model.
    """
    return SentenceTransformer(MODEL_NAME)