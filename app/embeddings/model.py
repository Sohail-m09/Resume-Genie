from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"


def get_embedding_model() -> SentenceTransformer:
    """
Load and return the configured embedding model.
SentenceTransformer embedding model.
    """
    return SentenceTransformer(MODEL_NAME)