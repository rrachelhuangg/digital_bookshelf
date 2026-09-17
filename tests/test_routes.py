import pytest

from app import books, create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    return app.test_client()


def test_index_renders_every_book(client):
    res = client.get("/")
    assert res.status_code == 200
    # One data-title per book, whatever books.json currently holds.
    assert res.data.count(b'data-title="') == len(books.all_books())


def test_unknown_url_404s(client):
    assert client.get("/nope").status_code == 404


def test_api_books(client):
    res = client.get("/api/books")
    assert res.status_code == 200
    payload = res.get_json()
    assert len(payload) == len(books.all_books())
    assert {"slug", "title", "author", "status"} <= payload[0].keys()


def test_healthz(client):
    assert client.get("/healthz").get_json() == {"status": "ok"}


def test_missing_cover_file_is_ignored():
    assert books.cover_file({"cover": "no-such-image.jpg"}) is None


def test_binding_is_stable_per_slug():
    assert books.binding("piranesi") == books.binding("piranesi")
    assert books.binding("piranesi") != books.binding("gathering-moss")
