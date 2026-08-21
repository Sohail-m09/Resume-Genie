from langchain_text_splitters import RecursiveCharacterTextSplitter
text = """
Python developer with experience in machine learning, SQL, FastAPI and Docker.

Built several machine learning projects using scikit-learn and XGBoost.

Developed REST APIs using FastAPI and deployed applications using Docker and AWS.

Worked with PostgreSQL, pandas and data visualization tools.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 150,
    chunk_overlap = 30
)

chunk = splitter.split_text(text)

print("Number of chunks : ", len(chunk))

for i, chunk in enumerate(chunk, start = 1):
    print(f"***** Chunk {i} *****")
    print(chunk)
    print("Characters", len(chunk))