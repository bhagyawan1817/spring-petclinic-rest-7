import os
import requests

ENDPOINT = "GET /api/vets"

BASE_URL = os.getenv(
    "BASE_URL",
    "http://localhost:9966/petclinic"
)

def test_get_vets():
    response = requests.get(f"{BASE_URL}/api/vets")
    assert response.status_code == 200
