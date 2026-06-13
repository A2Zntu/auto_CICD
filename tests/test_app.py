import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    rv = client.get("/")
    assert rv.status_code == 200


def test_index_contains_items(client):
    rv = client.get("/")
    assert b"Apple" in rv.data
    assert b"Banana" in rv.data


def test_health_ok(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["status"] == "ok"


def test_items_endpoint(client):
    rv = client.get("/items")
    assert rv.status_code == 200
    data = rv.get_json()
    assert "items" in data
    assert len(data["items"]) == 3
