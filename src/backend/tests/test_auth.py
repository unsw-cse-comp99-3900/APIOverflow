import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app import app 
from src.backend.classes.models import db

# Create a test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    """Fixture to clear the database before each test."""
    response = client.post("/testing/clear")
    assert response.status_code == 200


def test_register_user():
    """Test user registration."""
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email" : "doxxed@gmail.com"
    })
    assert response.status_code == 200
    assert response.json() == {"uid" : '0'}

def test_register_duplicate_user():
    """Test registering a duplicate user."""
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email" : "doxxed@gmail.com"
    })
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "newpassword",
        "email" : "doxxed@gmail.com"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already taken"}

def test_login_user():
    """Test user login."""
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email" : "doxxed@gmail.com"
    })
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user():
    """Test logging in with invalid credentials."""
    response = client.post("/auth/login", json={
        "username": "nonexistent",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}

def test_access_protected_route_as_user():
    """Test access to account route as a logged-in user."""
    client.post("/auth/register", json={
        "username": "user",
        "password": "password",
        "role": "account user",
        "email" : "doxxed@gmail.com"
    })
    response = client.post("/auth/login", json={
        "username": "user",
        "password": "password"
    })
    
    assert response.status_code == 200  
    access_token = response.json()["access_token"]

    response = client.get("/auth/account", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200 
    assert response.json() == {"message": "Welcome, Account User!"}


def test_access_protected_route_as_admin():
    """Test access to admin route."""
    # Register and login as admin
    client.post("/auth/register", json={
        "username": "adminuser",
        "password": "adminpassword",
        "role": "admin",
        "email" : "doxxed@gmail.com"
    })
    response = client.post("/auth/login", json={
        "username": "adminuser",
        "password": "adminpassword"
    })
    access_token = response.json()["access_token"]

    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome, Admin!"}


def test_access_protected_route_as_non_admin():
    """Test access to admin route as non-admin user."""
    # Register and login as guest
    client.post("/auth/register", json={
        "username": "guestuser",
        "password": "guestpassword",
        "email" : "doxxed@gmail.com"
    })
    response = client.post("/auth/login", json={
        "username": "guestuser",
        "password": "guestpassword"
    })
    access_token = response.json()["access_token"]

    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authorized"}
