from embeddings.similarity import semantic_similarity


pairs = [
    (
        "Bachelor's degree in Computer Science or a related field",
        "B.E. Computer Engineering",
    ),
    (
        "Bachelor's degree in Computer Science",
        "Bachelor's degree in Mechanical Engineering",
    ),
    (
        "Bachelor's degree in Computer Science",
        "B.E. Computer Engineering",
    ),
    (
        "Master's degree in Data Science",
        "Bachelor's degree in Computer Engineering",
    ),
]


for jd_requirement, candidate_education in pairs:

    score = semantic_similarity(
        jd_requirement,
        candidate_education,
    )

    print(
        f"\nJD: {jd_requirement}"
        f"\nResume: {candidate_education}"
        f"\nSimilarity: {score:.4f}"
    )