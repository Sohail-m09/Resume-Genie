from uuid import uuid4

from langchain_core.documents import Document

from database.config.database import SessionLocal

from database.models import (
    User,
    Resume,
    Job,
    Application,
)

from database.services.guest_session import (
    get_or_create_guest_user,
)

from database.repositories import (
    create_resume,
    create_job,
    create_application,
)

from vectorstore.chroma_store import (
    store_resume_chunks,
    get_chroma_collection,
)

from retrieval.chroma_retriever import (
    retrieve_resume_chunks,
)


db = SessionLocal()

session_1 = str(uuid4())
session_2 = str(uuid4())


try:

    # =================================================
    # USER 1
    # =================================================

    user_1 = get_or_create_guest_user(
        db=db,
        session_id=session_1,
    )

    resume_1 = create_resume(
        db=db,
        user_id=user_1.id,
        filename="user_1_resume.pdf",
        summary="Python and SQL Data Scientist.",
    )

    job_1 = create_job(
        db=db,
        user_id=user_1.id,
        job_title="Junior Data Scientist",
        company="Company A",
        source_type="text",
        required_skills=[
            "Python",
            "SQL",
        ],
    )

    application_1 = create_application(
        db=db,
        user_id=user_1.id,
        resume_id=resume_1.id,
        job_id=job_1.id,
        match_score=80.0,
        ats_score=85.0,
        analysis_result={
            "overall_score": 80.0,
        },
        tailored_resume={
            "summary": (
                "Python and SQL "
                "Data Scientist."
            ),
        },
    )

    store_resume_chunks(
        chunks=[
            Document(
                page_content=(
                    "User 1 has strong Python "
                    "and SQL experience."
                ),
                metadata={
                    "page": 0,
                    "page_label": "1",
                },
            )
        ],
        user_id=user_1.id,
        filename="user_1_resume.pdf",
    )

    # =================================================
    # USER 2
    # =================================================

    user_2 = get_or_create_guest_user(
        db=db,
        session_id=session_2,
    )

    resume_2 = create_resume(
        db=db,
        user_id=user_2.id,
        filename="user_2_resume.pdf",
        summary="Cybersecurity Engineer.",
    )

    job_2 = create_job(
        db=db,
        user_id=user_2.id,
        job_title="Cybersecurity Engineer",
        company="Company B",
        source_type="text",
        required_skills=[
            "Cybersecurity",
        ],
    )

    application_2 = create_application(
        db=db,
        user_id=user_2.id,
        resume_id=resume_2.id,
        job_id=job_2.id,
        match_score=70.0,
        ats_score=78.0,
        analysis_result={
            "overall_score": 70.0,
        },
        tailored_resume={
            "summary": (
                "Cybersecurity Engineer."
            ),
        },
    )

    store_resume_chunks(
        chunks=[
            Document(
                page_content=(
                    "User 2 has cybersecurity "
                    "and network security experience."
                ),
                metadata={
                    "page": 0,
                    "page_label": "1",
                },
            )
        ],
        user_id=user_2.id,
        filename="user_2_resume.pdf",
    )

    # =================================================
    # VERIFY POSTGRESQL ISOLATION
    # =================================================

    assert (
        resume_1.user_id == user_1.id
    )

    assert (
        resume_2.user_id == user_2.id
    )

    assert (
        job_1.user_id == user_1.id
    )

    assert (
        job_2.user_id == user_2.id
    )

    assert (
        application_1.user_id == user_1.id
    )

    assert (
        application_2.user_id == user_2.id
    )

    # =================================================
    # VERIFY CHROMADB ISOLATION
    # =================================================

    user_1_results = retrieve_resume_chunks(
        query="Python SQL",
        user_id=user_1.id,
        top_k=3,
    )

    user_2_results = retrieve_resume_chunks(
        query="cybersecurity",
        user_id=user_2.id,
        top_k=3,
    )

    user_1_metadata = (
        user_1_results["metadatas"][0]
    )

    user_2_metadata = (
        user_2_results["metadatas"][0]
    )

    assert all(
        metadata["user_id"] == user_1.id
        for metadata in user_1_metadata
    )

    assert all(
        metadata["user_id"] == user_2.id
        for metadata in user_2_metadata
    )

    # =================================================
    # VERIFY CROSS-USER BLOCKING
    # =================================================

    user_1_documents = (
        user_1_results["documents"][0]
    )

    user_2_documents = (
        user_2_results["documents"][0]
    )

    assert all(
        "User 2" not in document
        for document in user_1_documents
    )

    assert all(
        "User 1" not in document
        for document in user_2_documents
    )

    print(
        "User 1 PostgreSQL ownership verified."
    )

    print(
        "User 2 PostgreSQL ownership verified."
    )

    print(
        "User 1 ChromaDB isolation verified."
    )

    print(
        "User 2 ChromaDB isolation verified."
    )

    print(
        "Cross-user retrieval isolation verified."
    )

    print(
        "Full multi-user workflow test passed."
    )

finally:

    # =================================================
    # CLEAN CHROMADB
    # =================================================

    collection = get_chroma_collection()

    collection.delete(
        ids=[
            f"user_{user_1.id}_resume_chunk_1",
            f"user_{user_2.id}_resume_chunk_1",
        ]
    )

    # =================================================
    # CLEAN POSTGRESQL
    # =================================================

    db.query(Application).filter(
        Application.id.in_(
            [
                application_1.id,
                application_2.id,
            ]
        )
    ).delete(
        synchronize_session=False
    )

    db.query(Resume).filter(
        Resume.id.in_(
            [
                resume_1.id,
                resume_2.id,
            ]
        )
    ).delete(
        synchronize_session=False
    )

    db.query(Job).filter(
        Job.id.in_(
            [
                job_1.id,
                job_2.id,
            ]
        )
    ).delete(
        synchronize_session=False
    )

    db.query(User).filter(
        User.id.in_(
            [
                user_1.id,
                user_2.id,
            ]
        )
    ).delete(
        synchronize_session=False
    )

    db.commit()

    db.close()