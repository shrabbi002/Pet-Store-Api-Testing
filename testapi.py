import os
import pytest
import requests

BASE_URL = os.getenv("PETSTORE_API", "https://petstore.swagger.io/v2")
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Sample pet data
PET = {
    "id": 123456,
    "name": "test-pet",
    "photoUrls": [],
    "status": "available"
}

UPDATED_PET = {
    "id": PET["id"],
    "name": "updated-pet",
    "photoUrls": [],
    "status": "sold"
}

@pytest.fixture(scope="module")
def pet_id():
    return PET["id"]

def test_add_pet(pet_id):
    url = f"{BASE_URL}/pet"
    r = requests.post(url, headers=HEADERS, json=PET)
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == pet_id
    assert body["name"] == PET["name"]

def test_get_pet(pet_id):
    url = f"{BASE_URL}/pet/{pet_id}"
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == pet_id
    assert body["name"] == PET["name"]

def test_update_pet(pet_id):
    url = f"{BASE_URL}/pet"
    r = requests.put(url, headers=HEADERS, json=UPDATED_PET)
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == UPDATED_PET["name"]
    assert body["status"] == UPDATED_PET["status"]

def test_delete_pet(pet_id):
    url = f"{BASE_URL}/pet/{pet_id}"
    r = requests.delete(url, headers=HEADERS)
    assert r.status_code == 200

def test_get_deleted_pet(pet_id):
    url = f"{BASE_URL}/pet/{pet_id}"
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 404  # pet no longer exists
