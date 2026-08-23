def build_resume_context(retrieved_chunks: list[dict]) -> str:
    """
    Convert retrieved resume chunks into LLM-ready context.
    """

    context_parts = []

    for chunk in retrieved_chunks:
        text = chunk["text"]
        metadata = chunk.get("metadata", {})

        page = metadata.get("page_label") or metadata.get("page")

        if page is not None:
            context_parts.append(
                f"[Resume Page {page}]\n{text}"
            )
        else:
            context_parts.append(text)

    return "\n\n".join(context_parts)