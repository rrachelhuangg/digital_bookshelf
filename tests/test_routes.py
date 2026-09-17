import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    return app.test_client()


def test_index_lists_books(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Piranesi" in res.data


def test_book_detail(client):
    res = client.get("/book/piranesi")
    assert res.status_code == 200
    assert b"Susanna Clarke" in res.data


def test_unknown_book_404s(client):
    assert client.get("/book/nope").status_code == 404


def test_api_books(client):
    res = client.get("/api/books")
    assert res.status_code == 200
    assert len(res.get_json()) == 4


def test_healthz(client):
    assert client.get("/healthz").get_json() == {"status": "ok"}
