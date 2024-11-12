from fastapi.testclient import TestClient
import pytest

from app import app
from database import ( 
    truncate_table
)
from seeders import user_seeders

client = TestClient(app)


def test_login_for_access_token():
    truncate_table("user", True)
    user_seeders.seed()

    # act 
    response = client.post(
        "/token",
        data = {
            "username": "ann.ke",
            "password": "annpasswd"
        }
    )

    # Assert response
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"



    
