from embeddings.similarity import semantic_similarity


pairs = [
    (
        "Built REST APIs using FastAPI.",
        "Backend API development experience.",
    ),
    (
        "Deployed Docker containers to AWS.",
        "Cloud deployment and containerization experience.",
    ),
    (
        "Built a sales dashboard using Power BI.",
        "Backend API development experience.",
    ),
]


for project_description, job_requirement in pairs:

    score = semantic_similarity(
        project_description,
        job_requirement,
    )

    print(
        f"\nPROJECT: {project_description}"
        f"\nJD:      {job_requirement}"
        f"\nSimilarity: {score:.4f}"
    )