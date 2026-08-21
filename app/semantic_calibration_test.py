import csv

from embeddings.similarity import semantic_similarity


CSV_PATH = "data/semantic_skill_calibration.csv"


with open(CSV_PATH, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    rows = list(reader)


print("===== SEMANTIC CALIBRATION =====")

for row in rows:
    score = semantic_similarity(
        row["resume_skill"],
        row["job_requirement"],
    )

    print(
        f"{row['resume_skill']:15} <-> "
        f"{row['job_requirement']:30} | "
        f"label={row['label']} | "
        f"score={score:.4f}"
    )