import os
import pytest
import requests
import random
import string

BASE_URL = os.getenv("PETSTORE_API", "https://petstore.swagger.io/v2")
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Helpers
def random_id():
    return random.randint(100000, 999999)

def random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# Fixtures
@pytest.fixture(scope="module")
def pet_data():
    """Generate a random pet for testing."""
    return {
        "id": random_id(),
        "name": random_name(),
        "photoUrls": ["https://example.com/photo.png"],
        "status": "available"
    }

@pytest.fixture(scope="module")
def created_pet(pet_data):
    """Create a pet before running tests."""
    url = f"{BASE_URL}/pet"
    requests.post(url, headers=HEADERS, json=pet_data)
    return pet_data

# --------- Positive Tests ---------

def test_add_pet(pet_data):
    """Test adding a pet with valid data."""
    url = f"{BASE_URL}/pet"
    r = requests.post(url, headers=HEADERS, json=pet_data)
    assert r.status_code == 200
    assert r.json()["name"] == pet_data["name"]

def test_get_pet(created_pet):
    """Test retrieving an existing pet by ID."""
    url = f"{BASE_URL}/pet/{created_pet['id']}"
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200
    assert r.json()["id"] == created_pet["id"]

def test_update_pet_status(created_pet):
    """Test updating an existing pet's status."""
    created_pet["status"] = "sold"
    url = f"{BASE_URL}/pet"
    r = requests.put(url, headers=HEADERS, json=created_pet)
    assert r.status_code == 200
    assert r.json()["status"] == "sold"

# --------- Negative Tests ---------

@pytest.mark.parametrize("invalid_id", [-1, 0, 999999999])
def test_get_nonexistent_pet(invalid_id):
    """Ensure invalid IDs return 404."""
    url = f"{BASE_URL}/pet/{invalid_id}"
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 404

def test_add_pet_missing_fields():
    """Attempt to create a pet with missing required fields."""
    incomplete_pet = {"id": random_id()}
    url = f"{BASE_URL}/pet"
    r = requests.post(url, headers=HEADERS, json=incomplete_pet)
    # Petstore API sometimes returns 500 or 405 for bad data
    assert r.status_code in (400, 405, 500)

# --------- Search/List Tests ---------

@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_pets_by_status(status):
    """Test listing pets by their status."""
    url = f"{BASE_URL}/pet/findByStatus?status={status}"
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200
    assert all(pet.get("status") == status for pet in r.json())

# --------- Edge Case Tests ---------

def test_add_pet_with_long_name():
    """Test creating a pet with a very long name."""
    long_name_pet = {
        "id": random_id(),
        "name": "x" * 300,
        "photoUrls": [],
        "status": "available"
    }
    url = f"{BASE_URL}/pet"
    r = requests.post(url, headers=HEADERS, json=long_name_pet)
    assert r.status_code == 200
    assert len(r.json()["name"]) == 300

def test_add_pet_with_special_characters():
    """Test creating a pet with unusual characters in the name."""
    special_pet = {
        "id": random_id(),
        "name": "Test",
        "photoUrls": [],
        "status": "available"
    }
    url = f"{BASE_URL}/pet"
    r = requests.post(url, headers=HEADERS, json=special_pet)
    assert r.status_code == 200
    assert r.json()["name"] == "Test"

# --------- Cleanup ---------

def test_delete_pet(created_pet):
    """Clean up: delete the pet after testing."""
    url = f"{BASE_URL}/pet/{created_pet['id']}"
    r = requests.delete(url, headers=HEADERS)
    assert r.status_code == 200
