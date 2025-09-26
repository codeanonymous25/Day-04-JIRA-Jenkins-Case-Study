# test.py
import os
import importlib
import pytest

# Decide which module to test: 'app' (default) or 'app_bug'
MODULE_NAME = os.getenv("APP_UNDER_TEST", "app")
mod = importlib.import_module(MODULE_NAME)
app = getattr(mod, "app")

@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c

def test_home_200(client):
    rv = client.get("/")
    assert rv.status_code == 200

def test_roll_structure_and_totals(client):
    rv = client.get("/roll?count=3&faces=6&seed=123")
    assert rv.status_code == 200
    data = rv.get_json()
    assert {"count", "faces", "rolls", "total"} <= data.keys()
    assert data["count"] == 3
    assert data["faces"] == 6
    assert len(data["rolls"]) == 3
    assert sum(data["rolls"]) == data["total"]

def test_bounds_are_inclusive_1_to_faces(client):
    faces = 6
    rv = client.get(f"/roll?count=20&faces={faces}&seed=7")
    rolls = rv.get_json()["rolls"]
    assert all(1 <= r <= faces for r in rolls), "All rolls must be within [1, faces]"

def test_seed_is_deterministic(client):
    r1 = client.get("/roll?count=5&faces=8&seed=999").get_json()["rolls"]
    r2 = client.get("/roll?count=5&faces=8&seed=999").get_json()["rolls"]
    assert r1 == r2  # same seed => same sequence

def test_upper_face_can_appear(client):
    faces = 6
    # With enough rolls and a fixed seed, the top face should appear at least once
    rv = client.get(f"/roll?count=200&faces={faces}&seed=42")
    rolls = rv.get_json()["rolls"]
    assert faces in rolls, "The maximum face value should be possible"

def test_input_validation_errors(client):
    assert client.get("/roll?count=0&faces=6").status_code == 400
    assert client.get("/roll?count=2&faces=1").status_code == 400
    assert client.get("/roll?count=abc&faces=6").status_code == 400
    assert client.get("/roll?count=2&faces=xyz").status_code == 400
    assert client.get("/roll?count=2&faces=6&seed=notint").status_code == 400
