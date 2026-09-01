from typing import Any


def add_user_metadata(
    metadata: dict[str, Any],
    user_id: int,
) -> dict[str, Any]:
    """
    Add user ownership information to existing
    ChromaDB chunk metadata.
    """

    enriched_metadata = dict(metadata)

    enriched_metadata["user_id"] = user_id

    return enriched_metadata


def build_user_filter(
    user_id: int,
) -> dict[str, Any]:
    """
    Build a ChromaDB metadata filter for user isolation.
    """

    return {
        "user_id": user_id
    }
