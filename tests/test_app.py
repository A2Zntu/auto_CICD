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


def test_index_contains_bs_form(client):
    rv = client.get("/")
    assert b"Black-Scholes" in rv.data
    assert b'name="S"' in rv.data
    assert b'name="sigma"' in rv.data


def test_health_ok(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "ok"


def test_post_returns_call_and_put(client):
    rv = client.post("/", data={"S": 100, "K": 100, "T": 1, "r": 0.05, "sigma": 0.20})
    assert rv.status_code == 200
    assert b"Call Option" in rv.data
    assert b"Put Option" in rv.data
