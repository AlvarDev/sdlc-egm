import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture(autouse=True)
def reset_state() -> None:
    main.cards_db.clear()
    main.next_id = 1


client = TestClient(main.app)


def test_serve_index() -> None:
    res = client.get("/")
    assert res.status_code == 200
    assert "RetroPulse" in res.text


def test_create_and_list_cards() -> None:
    res = client.post(
        "/api/cards",
        json={"text": "  Shipped v1 cleanly  ", "category": "Went Well"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data == {
        "id": 1,
        "text": "Shipped v1 cleanly",
        "category": "Went Well",
        "votes": 0,
    }

    list_res = client.get("/api/cards")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1


def test_reject_whitespace_only_and_long_text() -> None:
    blank_res = client.post(
        "/api/cards",
        json={"text": "   ", "category": "To Improve"},
    )
    assert blank_res.status_code == 422

    long_res = client.post(
        "/api/cards",
        json={"text": "x" * 281, "category": "Action Items"},
    )
    assert long_res.status_code == 422


def test_upvote_card_and_not_found() -> None:
    created = client.post(
        "/api/cards",
        json={"text": "Automate CI gates", "category": "Action Items"},
    ).json()

    up_res = client.post(f"/api/cards/{created['id']}/upvote")
    assert up_res.status_code == 200
    assert up_res.json()["votes"] == 1

    missing_res = client.post("/api/cards/999/upvote")
    assert missing_res.status_code == 404
