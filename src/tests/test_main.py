from fastapi.testclient import TestClient


from src.main import app

client = TestClient(app)

base_request = {
    "cart_value": 790,
    "delivery_distance": 2235,
    "number_of_items": 4,
    "time": "2024-01-15T13:00:00Z",
}

input_should_be_int = (
    "Input should be a valid integer, unable to parse string as an integer"
)

input_should_be_ge_zero = "Input should be greater than 0"

input_should_be_str = "Input should be a valid string"

input_should_be_UTC_ISO = "Value error, Date must be UTC in ISO format"


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
    assert response.json()["detail"][0]["msg"] == input_should_be_int
    assert response.json()["detail"][0]["loc"][1] == "cart_value"


def test_calculate_fee_endpoint_incorrect_cart_value_negative():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "cart_value": -2},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == input_should_be_ge_zero
    assert response.json()["detail"][0]["loc"][1] == "cart_value"


def test_calculate_fee_endpoint_incorrect_delivery_distance_str():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "delivery_distance": "incorrect value"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == input_should_be_int
    assert response.json()["detail"][0]["loc"][1] == "delivery_distance"


def test_calculate_fee_endpoint_incorrect_delivery_distance_negative():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "delivery_distance": -2},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == input_should_be_ge_zero
    assert response.json()["detail"][0]["loc"][1] == "delivery_distance"


def test_calculate_fee_endpoint_incorrect_items_str():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "number_of_items": "incorrect value"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == input_should_be_int
    assert response.json()["detail"][0]["loc"][1] == "number_of_items"


def test_calculate_fee_endpoint_incorrect_items_negative():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "number_of_items": -2},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == input_should_be_ge_zero
    assert response.json()["detail"][0]["loc"][1] == "number_of_items"


def test_calculate_fee_endpoint_time_int():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "time": 1},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == input_should_be_str
    assert response.json()["detail"][0]["loc"][1] == "time"


def test_calculate_fee_endpoint_time_not_UTC_ISO():
    response = client.post(
        "/api/calculate_delivery_fee",
        json={**base_request, "time": "2024-10-10-13:00"},
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == input_should_be_UTC_ISO
    assert response.json()["detail"][0]["loc"][1] == "time"
