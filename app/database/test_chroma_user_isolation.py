from database.services.chroma_user_service import (
    add_user_metadata,
    build_user_filter,
)


def test_user_metadata_is_added():
    metadata = {
        "source": "resume.pdf",
        "page": 1,
        "page_label": "1",
    }

    enriched = add_user_metadata(
        metadata=metadata,
        user_id=101,
    )

    assert enriched["user_id"] == 101
    assert enriched["source"] == "resume.pdf"
    assert enriched["page"] == 1
    assert enriched["page_label"] == "1"


def test_user_filter_is_correct():
    result = build_user_filter(
        user_id=101
    )

    assert result == {
        "user_id": 101
    }


def test_users_have_different_filters():
    user_1_filter = build_user_filter(
        user_id=101
    )

    user_2_filter = build_user_filter(
        user_id=202
    )

    assert user_1_filter != user_2_filter