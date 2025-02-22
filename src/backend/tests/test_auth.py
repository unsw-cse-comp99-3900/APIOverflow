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
        "displayname": "testuser",
        "username": "testuser",
        "password": "testpassword",
        "email" : "doxxed@gmail.com"
    })
    assert response.status_code == 200
    assert response.json() == {"uid" : '1'}

def test_register_duplicate_user():
    """Test registering a duplicate user."""
    client.post("/auth/register", json={
        "displayname": "testuser",
        "username": "testuser",
        "password": "testpassword",
        "email" : "doxxed@gmail.com"
    })
    response = client.post("/auth/register", json={
        "displayname": "testuser",
        "username": "testuser",
        "password": "newpassword",
        "email" : "doxxed@gmail.com"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already taken"}

def test_login_user():
    """Test user login."""
    client.post("/auth/register", json={
        "displayname": "testuser",
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
        "displayname": "testuser",
        "username": "user",
        "password": "password",
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
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    access_token = response.json()["access_token"]

    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome, Admin!"}


def test_access_protected_route_as_non_admin():
    """Test access to admin route as non-admin user."""
    # Register and login as guest
    client.post("/auth/register", json={
        "displayname": "guestuser",
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

def test_reaccess_after_logout_and_login():
    """Test login, logout and login again access"""
    # Register and login as admin
    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    access_token0 = response.json()["access_token"]

    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {access_token0}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome, Admin!"}

    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {access_token0}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}

    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {access_token0}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Current token is invalid"}

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    access_token1 = response.json()["access_token"]
    # assert access_token0 != access_token1

    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {access_token1}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome, Admin!"}

def test_reaccess_after_logout_and_login_more():
    """Test login, logout and login again access for multiple users"""
    # Register and login as guest
    client.post("/auth/register", json={
        "displayname": "guestuser",
        "username": "guestuser",
        "password": "guestpassword",
        "email" : "doxxed1@gmail.com"
    })
    response = client.post("/auth/login", json={
        "username": "guestuser",
        "password": "guestpassword"
    })
    assert response.status_code == 200  
    access_token0 = response.json()["access_token"]

    client.post("/auth/register", json={
        "displayname": "guestuser",
        "username": "guestuser1",
        "password": "guestpassword",
        "email" : "doxxed2@gmail.com"
    })
    response = client.post("/auth/login", json={
        "username": "guestuser1",
        "password": "guestpassword"
    })
    assert response.status_code == 200  
    access_token1 = response.json()["access_token"]

    response = client.get("/auth/account", headers={"Authorization": f"Bearer {access_token0}"})
    assert response.status_code == 200 
    assert response.json() == {"message": "Welcome, Account User!"}

    response = client.get("/auth/account", headers={"Authorization": f"Bearer {access_token1}"})
    assert response.status_code == 200 
    assert response.json() == {"message": "Welcome, Account User!"}

    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {access_token0}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}

    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {access_token1}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}

    response = client.get("/auth/account", headers={"Authorization": f"Bearer {access_token0}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Current token is invalid"}

    response = client.get("/auth/account", headers={"Authorization": f"Bearer {access_token1}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Current token is invalid"}

    response = client.post("/auth/login", json={
        "username": "superadmin",
        "password": "superadminpassword"
    })
    access_token0 = response.json()["access_token"]

    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {access_token0}"})
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully logged out"}

    response = client.get("/auth/admin", headers={"Authorization": f"Bearer {access_token0}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Current token is invalid"}

def test_register_duplicate_email():
    """Test registering a duplicate user."""
    client.post("/auth/register", json={
        "displayname": "testuser",
        "username": "testuser1",
        "password": "testpassword",
        "email" : "doxxed@gmail.com"
    })
    response = client.post("/auth/register", json={
        "displayname": "testuser",
        "username": "testuser2",
        "password": "newpassword",
        "email" : "doxxed@gmail.com"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}