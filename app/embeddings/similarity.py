from sklearn.metrics.pairwise import cosine_similarity

from embeddings.model import get_embedding_model


def semantic_similarity(
    text_a: str,
    text_b: str,
) -> float:
    """
    Calculate cosine similarity between two text inputs.

    Args:
        text_a: First text.
        text_b: Second text.

    Returns:
        Cosine similarity score.
    """
    model = get_embedding_model()

    embeddings = model.encode(
        [text_a, text_b],
        normalize_embeddings=True,
    )

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]],
    )[0][0]

    return float(score)