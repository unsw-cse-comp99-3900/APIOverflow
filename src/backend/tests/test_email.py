import pytest
from src.backend.server.auth import send_email, generate_verification_token
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app import app 
from src.backend.classes.datastore import data_store
from unittest.mock import patch, MagicMock
from src.backend.classes.User import User
import base64
import os

# Create a test client
client = TestClient(app)
from dotenv import load_dotenv

# Load .env file
load_dotenv()

@pytest.fixture(autouse=True)
def set_email_env():
    os.environ["EMAIL"] = "True"
    yield 
    os.environ["EMAIL"] = "False"

@pytest.fixture(autouse=True)
def clear_database():
    """Fixture to clear the database before each test."""
    response = client.post("/testing/clear")
    assert response.status_code == 200

@pytest.fixture
def mock_email_setup():
    mock_credentials = MagicMock()
    mock_service = MagicMock()
    with patch('src.backend.server.auth.build', return_value=mock_service) as mock_build, \
         patch('src.backend.server.auth.get_credentials', return_value=mock_credentials) as mock_get_credentials:
        yield mock_get_credentials, mock_build, mock_service, mock_credentials

email = os.getenv("EMAIL", "False")
def test_email_set():
    assert email

def test_send_ver_email(mock_email_setup):
    mock_get_credentials, mock_build, mock_service, mock_credentials = mock_email_setup
    mock_service.users().messages().send.return_value.execute.return_value = {'id': '12345'}

    to_email = "test@example.com"
    token = "test_token"

    result = send_email(to_email, token, email_type='verification')

    assert result == {'id': '12345'}
    mock_get_credentials.assert_called_once()
    mock_build.assert_called_once_with('gmail', 'v1', credentials=mock_credentials)
    mock_service.users().messages().send.assert_called_once() 

def test_send_pass_email(mock_email_setup):
    mock_get_credentials, mock_build, mock_service, mock_credentials = mock_email_setup
    mock_service.users().messages().send.return_value.execute.return_value = {'id': '12345'}

    to_email = "test@example.com"
    token = "test_token"

    result = send_email(to_email, token, email_type='password_reset')

    assert result == {'id': '12345'}
    mock_get_credentials.assert_called_once()
    mock_build.assert_called_once_with('gmail', 'v1', credentials=mock_credentials)
    mock_service.users().messages().send.assert_called_once() 


def test_send_ver_email_route():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email" : "test@gmail.com"
    })
    assert response.status_code == 200

def test_send_pass_email_route():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email" : "test@gmail.com"
    })
    assert response.status_code == 200
    uid = response.json()['uid']
    user = data_store.get_user_by_id(uid)
    user.verify_user()

    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    
    assert response.status_code == 200  
    access_token = response.json()["access_token"]

    response = client.post(f"/auth/reset-password", headers={"Authorization": f"Bearer {access_token}"})
    assert response.json() == {"message": "Password reset email sent."}

def test_verify_email():

    new_user = User("12",
                    "user",
                    "what",
                    "huh",
                    False,
                    False)
    data_store.add_user(new_user)
    user = data_store.get_user_by_id("12")
    verification_token = generate_verification_token("12") 
    assert user.get_is_verified() == False

    response = client.get(f"/auth/verify-email/{verification_token}")

    user = data_store.get_user_by_id("12")
    assert user.get_is_verified() == True
    assert response.status_code == 200
    assert response.json() == {"message": "Email verified successfully."}

def test_reset_password():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email" : "test@gmail.com"
    })
    assert response.status_code == 200
    uid = response.json()['uid']
    user = data_store.get_user_by_id(uid)
    user.verify_user()

    verification_token = generate_verification_token("1")
    response = client.post(f"/auth/reset-password/{verification_token}", 
                            json={
                              'newpass' : "newpassword"
                            })

    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 400

    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "newpassword"
    })
    assert response.status_code == 200

def test_bad_token():

    verification_token = 'what'
    response = client.post(f"/auth/reset-password/{verification_token}", 
                            json={
                              'newpass' : "newpassword"
                            })
    assert response.status_code == 400
    response = client.post(f"/auth/reset-password/{verification_token}", 
                            json={
                              'newpass' : "newpassword"
                            })
    assert response.status_code == 400