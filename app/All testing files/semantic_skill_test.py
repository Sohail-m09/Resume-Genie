from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("BAAI/bge-small-en-v1.5")

resume_skills = [
    "FastAPI",
    "Python",
    "Docker",
]

job_skills = [
    "Backend API development",
    "Python programming",
    "Containerization",
]


resume_embeddings = model.encode(
    resume_skills,
    normalize_embeddings=True,
)

job_embeddings = model.encode(
    job_skills,
    normalize_embeddings=True,
)


print("===== SEMANTIC SKILL MATCHING =====")

for i, resume_skill in enumerate(resume_skills):

    for j, job_skill in enumerate(job_skills):

        similarity = cosine_similarity(
            [resume_embeddings[i]],
            [job_embeddings[j]],
        )[0][0]

        print(
            f"{resume_skill:15} <-> "
            f"{job_skill:25} = "
            f"{similarity:.4f}"
        )