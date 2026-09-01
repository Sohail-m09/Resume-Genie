from uuid import uuid4

from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_unknown_session_history_is_empty():
    session_id = str(
        uuid4()
    )

    response = client.get(
        "/api/history/applications",
        headers={
            "X-Session-ID": session_id
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 0
    assert data["applications"] == []
    assert "user_id" not in data