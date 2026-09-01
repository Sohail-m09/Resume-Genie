from langchain_core.documents import Document

from vectorstore.chroma_store import (
    store_resume_chunks,
    get_chroma_collection,
)

from retrieval.chroma_retriever import (
    retrieve_resume_chunks,
)


USER_1 = 101
USER_2 = 202

USER_1_FILENAME = "user_101_resume_test.pdf"
USER_2_FILENAME = "user_202_resume_test.pdf"


user_1_chunks = [
    Document(
        page_content=(
            "User 101 is a Data Scientist with strong "
            "Python, SQL, Pandas, and machine learning "
            "experience."
        ),
        metadata={
            "page": 1,
            "page_label": "1",
        },
    ),
]

user_2_chunks = [
    Document(
        page_content=(
            "User 202 is a Cybersecurity Engineer with "
            "network security, penetration testing, and "
            "security monitoring experience."
        ),
        metadata={
            "page": 1,
            "page_label": "1",
        },
    ),
]


collection = get_chroma_collection()

user_1_ids = [
    f"user_{USER_1}_resume_chunk_1"
]

user_2_ids = [
    f"user_{USER_2}_resume_chunk_1"
]


try:

    # -----------------------------------------------
    # Store User 101 resume
    # -----------------------------------------------

    store_resume_chunks(
        chunks=user_1_chunks,
        user_id=USER_1,
        filename=USER_1_FILENAME,
    )

    # -----------------------------------------------
    # Store User 202 resume
    # -----------------------------------------------

    store_resume_chunks(
        chunks=user_2_chunks,
        user_id=USER_2,
        filename=USER_2_FILENAME,
    )

    # -----------------------------------------------
    # Retrieve as User 101
    # -----------------------------------------------

    user_1_results = retrieve_resume_chunks(
        query="Python and SQL experience",
        user_id=USER_1,
        top_k=3,
    )

    user_1_metadata = (
        user_1_results["metadatas"][0]
    )

    user_1_documents = (
        user_1_results["documents"][0]
    )

    assert all(
        metadata["user_id"] == USER_1
        for metadata in user_1_metadata
    )

    assert all(
        USER_2_FILENAME
        not in document
        for document in user_1_documents
    )

    # -----------------------------------------------
    # Retrieve as User 202
    # -----------------------------------------------

    user_2_results = retrieve_resume_chunks(
        query="network security experience",
        user_id=USER_2,
        top_k=3,
    )

    user_2_metadata = (
        user_2_results["metadatas"][0]
    )

    user_2_documents = (
        user_2_results["documents"][0]
    )

    assert all(
        metadata["user_id"] == USER_2
        for metadata in user_2_metadata
    )

    assert all(
        USER_1_FILENAME
        not in document
        for document in user_2_documents
    )

    print(
        "User 101 retrieval isolated successfully."
    )

    print(
        "User 202 retrieval isolated successfully."
    )

    print(
        "ChromaDB multi-user isolation test passed."
    )

finally:

    # -----------------------------------------------
    # Cleanup test records
    # -----------------------------------------------

    collection.delete(
        ids=user_1_ids + user_2_ids
    )