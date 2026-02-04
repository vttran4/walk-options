from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


def test_optimize_endpoint():
    payload = {
        "rows": [
            {"Stock": "A", "Collateral": 100, "Premium": 10},
            {"Stock": "B", "Collateral": 200, "Premium": 30},
        ],
        "collateral_limit": 200,
    }

    resp = client.post("/optimize", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["total_premium"] == 30
    assert data["total_collateral"] == 200
    assert len(data["selected"]) == 1
    assert data["selected"][0]["Stock"] == "B"
