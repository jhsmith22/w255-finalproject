import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from numpy.testing import assert_almost_equal
from src.main import app


@pytest.fixture
def client():
    FastAPICache.init(InMemoryBackend())
    with TestClient(app) as c:
        yield c


def test_predict(client):
    data = {"text": ["I hate you.", "I love you."]}
    response = client.post(
        "/predict",
        json=data,
    )

    assert response.status_code == 200
    assert type(response.json()["predictions"]) is list
    assert type(response.json()["predictions"][0]) is list
    assert type(response.json()["predictions"][0][0]) is dict
    assert type(response.json()["predictions"][1][0]) is dict
    assert set(response.json()["predictions"][0][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][0][1].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][0].keys()) == {"label", "score"}
    assert set(response.json()["predictions"][1][1].keys()) == {"label", "score"}
    assert response.json()["predictions"][0][0]["label"] == "NEGATIVE"
    assert response.json()["predictions"][0][1]["label"] == "POSITIVE"
    assert response.json()["predictions"][1][0]["label"] == "NEGATIVE"
    assert response.json()["predictions"][1][1]["label"] == "POSITIVE"
    assert (
        assert_almost_equal(
            response.json()["predictions"][0][0]["score"], 0.900, decimal=3
        )
        is None
    )
    assert (
        assert_almost_equal(
            response.json()["predictions"][0][1]["score"], 0.099, decimal=3
        )
        is None
    )
    assert (
        assert_almost_equal(
            response.json()["predictions"][1][0]["score"], 0.003, decimal=3
        )
        is None
    )
    assert (
        assert_almost_equal(
            response.json()["predictions"][1][1]["score"], 0.996, decimal=3
        )
        is None
    )

# If we send in a bad type do we fail validation?
# We see that if we send a list of integers, it still tokenizes to strings
def test_predict_bad_type(client):
    data = {"text": [5, 6]}

    response = client.post(
        "/predict",
        json=data,
    )

    assert response.status_code == 200

# If we send a blank list, it still works
def test_predict_nulls(client):
    data = {"text": []}

    response = client.post(
        "/predict",
        json=data,
    )
    assert response.status_code == 200


# If we send a string instead of a list of strings, it fails
# Returns 422, unproccessable content
def test_predict_bad_format_string(client):
    data = {"text": "I hate you."}

    response = client.post(
        "/predict",
        json=data,
    )

    assert response.status_code == 422

# If we send a integer instead of a list of strings, it fails
# Returns 422, unproccessable content
def test_predict_bad_format_int(client):
    data = {"text": 1}

    response = client.post(
        "/predict",
        json=data,
    )

    assert response.status_code == 422


# If we send the wrong key, it fails.
# Returns 422, unprocessable content
def test_predict_bad_key(client):
    data = {"words": ["I hate you."]}

    response = client.post(
        "/predict",
        json=data,
    )
    assert response.status_code == 422

# If we send extra feature
# Returns 422, unprocessable content
def test_predict_extra_feature(client):
    data = {"text": ["I hate you."], "cake": ["I love you"]}

    response = client.post(
        "/predict",
        json=data,
    )
    assert response.status_code == 422