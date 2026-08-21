from embeddings.similarity import semantic_similarity


pairs = [
    ("Python", "Python programming"),
    ("Docker", "Containerization"),
    ("FastAPI", "Backend API development"),
    ("Docker", "Accounting"),
]


for text_a, text_b in pairs:

    score = semantic_similarity(
        text_a,
        text_b,
    )

    print(
        f"{text_a:30} <-> "
        f"{text_b:30} = "
        f"{score:.4f}"
    )