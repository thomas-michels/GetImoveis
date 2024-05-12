from app.api.composers import address_composer
from tests.api.routes import client
from unittest.mock import AsyncMock

def test_create_address():
    address_data = {
        "street": "Test Street",
        "neighborhood": "Test Neighborhood",
        "zip_code": "12345-678",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }
    address_data_in_db = address_data.copy()
    address_data_in_db["id"] = 1

    mock = AsyncMock()
    mock.create.return_value = address_data_in_db

    response = client(mock=mock, overrides=address_composer).post("/address", json=address_data)
    assert response.status_code == 200
    created_address = response.json()
    assert "id" in created_address
    assert created_address["street"] == "Test Street"

def test_create_address_error():
    address_data = {
        "street": "Test Street",
        "neighborhood": "Test Neighborhood",
        "zip_code": "12345-678",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }

    mock = AsyncMock()
    mock.create.return_value = None

    response = client(mock=mock, overrides=address_composer).post("/address", json=address_data)
    assert response.status_code == 400

def test_get_address():
    mock = AsyncMock()
    mock.search_all.return_value = [{
        "street": "Test Street",
        "neighborhood": "Test Neighborhood",
        "zip_code": "12345-678",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }]

    response = client(mock=mock, overrides=address_composer).get("/address")

    assert response.status_code == 200
    addresses = response.json()
    assert len(addresses) > 0

def test_get_address_by_zip_code():
    mock = AsyncMock()
    mock.search_by_zip_code.return_value = {
        "street": "Test Street",
        "neighborhood": "Test Neighborhood",
        "zip_code": "12345-678",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }

    response = client(mock=mock, overrides=address_composer).get("/address/zip-code/12345-678")
    assert response.status_code == 200
    address = response.json()
    assert address["zip_code"] == "12345-678"

def test_get_address_by_street():
    mock = AsyncMock()
    mock.search_by_street.return_value = {
        "street": "Test Street",
        "neighborhood": "Test Neighborhood",
        "zip_code": "12345-678",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }

    response = client(mock=mock, overrides=address_composer).get("/address/street/Test%20Street")
    assert response.status_code == 200
    address = response.json()
    assert address["street"] == "Test Street"

def test_get_address_by_neighborhood():
    mock = AsyncMock()
    mock.search_by_neighborhood.return_value = {
        "street": "Test Street",
        "neighborhood": "Test Neighborhood",
        "zip_code": "12345-678",
        "flood_quota": None,
        "latitude": None,
        "longitude": None,
    }

    response = client(mock=mock, overrides=address_composer).get("/address/neighborhood/Test%20Neighborhood")
    assert response.status_code == 200
    address = response.json()
    assert address["neighborhood"] == "Test Neighborhood"
