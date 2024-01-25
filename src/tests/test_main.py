from fastapi.testclient import TestClient


from src.main import app

client = TestClient(app)

base_request = {
    "cart_value": 790,
    "delivery_distance": 2235,
    "number_of_items": 4,
    "time": "2024-01-15T13:00:00Z",
}


def test_server_is_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running"}


def test_calculate_fee_endpoint_correct_values():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request},
    )
    assert response.status_code == 200
    assert response.json() == {"delivery_fee": 710}


def test_calculate_fee_endpoint_incorrect_cart_value_str():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "cart_value": "incorrect value"},
    )
    assert response.status_code == 422


def test_calculate_fee_endpoint_incorrect_cart_value_negative():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "cart_value": -2},
    )
    assert response.status_code == 422


def test_calculate_fee_endpoint_incorrect_delivery_distance_str():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "delivery_distance": "incorrect value"},
    )
    assert response.status_code == 422


def test_calculate_fee_endpoint_incorrect_delivery_distance_negative():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "delivery_distance": -2},
    )
    assert response.status_code == 422


def test_calculate_fee_endpoint_incorrect_items_str():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "number_of_items": "incorrect value"},
    )
    assert response.status_code == 422


def test_calculate_fee_endpoint_incorrect_items_negative():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "number_of_items": -2},
    )
    assert response.status_code == 422


def test_calculate_fee_endpoint_time_int():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "time": 1},
    )
    assert response.status_code == 422


def test_calculate_fee_endpoint_time_not_UTC_ISO():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "time": "2024-10-10-13:00"},
    )
    assert response.status_code == 422
