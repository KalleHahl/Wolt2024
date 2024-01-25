from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_server_is_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running"}


def test_calculate_fee_endpoint():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2024-01-15T13:00:00Z",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}
