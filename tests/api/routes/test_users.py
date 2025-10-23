from fastapi.testclient import TestClient
from datetime import datetime

def test_register_user(client_with_superuser: TestClient):
    user_data = {
        "username": "Test User1",
        "email": "user1@test.com",
        "password": "Kennwort1"
    }

    response = client_with_superuser.post("/api/users/register", json=user_data)
    assert response.status_code == 200


