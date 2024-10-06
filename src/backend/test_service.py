import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from app import app
from models import User, db, Service
from helper import *

# Create a test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    """Fixture to clear the database before each test."""
    db.users.delete_many({})
    db.services.delete_many({})

@pytest.fixture
def setup_service_provider():
    """Fixture to register and log in as a service provider."""
    client.post("/auth/register", json={
        "username": test_provider()["username"],
        "email": test_provider()["email"],
        "password": test_provider()["password"],
        "role": test_provider()["role"]
    })
    login_response = client.post("/auth/login", json={
        "username": test_provider()["username"],
        "password": test_provider()["password"],
    })
    access_token = login_response.json()["access_token"]
    return access_token

def test_manage_services(setup_service_provider):
    """Test managing services as a service provider."""
    access_token = setup_service_provider
    response = client.get("/service/manage", headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]
    assert "services" in response.json()

def test_create_service(setup_service_provider):
    """Test creating a service as a service provider."""
    access_token = setup_service_provider
    service_data = {
        "name": "Test Service",
        "documentation": "Test Service",
        "endpoint": "Test Service"
    }
    response = client.post("/service/create", json=service_data, headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "Service 'Test Service' created by serviceprovider."

    created_service = Service.get_service_by_id(response.json()["service_id"], db)
    assert created_service["name"] == service_data["name"]
    assert created_service["documentation"] == service_data["documentation"]
    assert created_service["endpoint"] == service_data["endpoint"]
    assert created_service["provider_username"] == test_provider()["username"]

def test_delete_service(setup_service_provider):
    """Test deleting a service as a service provider."""
    access_token = setup_service_provider
    service_data = {
        "name": "Test Service",
        "documentation": "Test Service",
        "endpoint": "Test Service"
    }
    create_response = client.post("/service/create", json=service_data, headers={"Authorization": f"Bearer {access_token}"})
    
    service_id = create_response.json()["service_id"]

    delete_response = client.delete(f"/service/delete/{service_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Service deleted successfully"}

def test_delete_service_not_found(setup_service_provider):
    """Test deleting a service that does not exist."""
    access_token = setup_service_provider
    response = client.delete("/service/delete/invalid_service_id", headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Service not found"}

def test_delete_service_not_authorized(setup_service_provider):
    """Test trying to delete a service that the user does not own."""
    access_token = setup_service_provider

    service_data = {
        "name": "Test Service",
        "documentation": "Test Service",
        "endpoint": "Test Service"
    }
    create_response = client.post("/service/create", json=service_data, headers={"Authorization": f"Bearer {access_token}"})

    client.post("/auth/register", json={
        "username": test_guest()["username"],
        "email": test_guest()["email"],
        "password": test_guest()["password"],
        "role": test_guest()["role"]
    })
    login_response = client.post("/auth/login", json={
        "username": test_guest()["username"],
        "password": test_guest()["password"],
    })
    guest_access_token = login_response.json()["access_token"]

    # Attempt to delete the service
    service_id = create_response.json()["service_id"]
    delete_response = client.delete(f"/service/delete/{service_id}", headers={"Authorization": f"Bearer {guest_access_token}"})
    
    assert delete_response.status_code == 403
    assert delete_response.json() == {"detail": "Not authorized"}
