import pytest
from src.backend.server.auth import send_email, generate_verification_token
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app import app 
from src.backend.classes.datastore import data_store
from unittest.mock import patch, MagicMock
from src.backend.classes.User import User

# Create a test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    """Fixture to clear the database before each test."""
    response = client.post("/testing/clear")
    assert response.status_code == 200

@pytest.fixture
def mock_email_settings():
    return {
        'email': 'test@gmail.com',
        'verification_token': 'test_token'
    }

@patch('smtplib.SMTP_SSL')
def test_send_verification_email(mock_smtp_ssl, mock_email_settings):
    email = mock_email_settings['email']
    verification_token = mock_email_settings['verification_token']

    mock_smtp_instance = mock_smtp_ssl.return_value.__enter__.return_value
    mock_smtp_instance.login = MagicMock()
    mock_smtp_instance.sendmail = MagicMock()

    send_email(email, verification_token)

    mock_smtp_ssl.assert_called_once_with('smtp.gmail.com', 465)
    mock_smtp_instance.login.assert_called_once_with("api.overflow6@gmail.com", "itdobeflowing")
    mock_smtp_instance.sendmail.assert_called_once()
    
    args, _ = mock_smtp_instance.sendmail.call_args
    assert args[1] == email
    assert 'verify-email/test_token' in args[2]

@patch('smtplib.SMTP_SSL')
def test_send_passreset_email(mock_smtp_ssl, mock_email_settings):
    email = mock_email_settings['email']
    verification_token = mock_email_settings['verification_token']

    mock_smtp_instance = mock_smtp_ssl.return_value.__enter__.return_value
    mock_smtp_instance.login = MagicMock()
    mock_smtp_instance.sendmail = MagicMock()

    send_email(email, verification_token, 'password_reset')

    mock_smtp_ssl.assert_called_once_with('smtp.gmail.com', 465)
    mock_smtp_instance.login.assert_called_once_with("api.overflow6@gmail.com", "itdobeflowing")
    mock_smtp_instance.sendmail.assert_called_once()
    
    args, _ = mock_smtp_instance.sendmail.call_args
    assert args[1] == email
    assert 'reset-password/test_token' in args[2]

def test_send_email():
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "email" : "test@gmail.com"
    })
    assert response.status_code == 200

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